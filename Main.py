import Logger
from configparser import ConfigParser
import Actions
import Game_Database
import json
from os import path
import os
import time
import re
import Video_Post_Processing


def get_mozilla_with_extension_enabled():
    '''
    This method enables the gecko driver with required preferences.
    Like download on current working directory
    :return: driver
    '''
    from selenium import webdriver
    from os import path
    firefox_options = webdriver.FirefoxOptions()
    try:
        if path.exists('gameslist.csv'):
            os.remove('gameslist.csv')
    except Exception as ee:
        pass

    # 0 means to download to the desktop, 1 means to download to the default "Downloads" directory, 2 means to use the directory
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.dir", path.abspath(path.curdir))
    firefox_options.set_preference("browser.download.useDownloadDir", True);
    firefox_options.set_preference("browser.download.viewableInternally.enabledTypes", "");
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                   "application/pdf;text/plain;application/text;text/xml;application/xml;application/csv;text/csv;application/octet-stream");
    firefox_options.set_preference("pdfjs.disabled", True);
    firefox_options.headless = CONFIG_OBJ.get('headless_browser')
    try:
        driver = webdriver.Firefox(executable_path=CONFIG_OBJ.get('gecko_driver_path'), options=firefox_options)
        logger.debug("Gecko driver loaded successfully")
    except Exception as ee:
        driver_abs_path = path.abspath(CONFIG_OBJ.get('gecko_driver_path'))
        logger.error("Gecko driver not loaded, Trying to load from the absolute path now")
        try:
            driver = webdriver.Firefox(executable_path=driver_abs_path, options=firefox_options)
            logger.debug("Gecko driver loaded from absolute path")
        except Exception as e:
            logger.error("Can't load gecko driver- {}".format(e))
            return None
    return driver


def main(driver, ACTIONS_LIST):
    ae_obj = Actions.ActionExecutables(driver, logger)
    vp_obj = Video_Post_Processing.VideoProcessing(CONFIG_OBJ)
    db_obj = None
    if not CONFIG_OBJ.get('skip_database_file', False):
        db_obj = Game_Database.Game_Database(CONFIG_OBJ.get('database_file_path'), logger)

    start_actions = [
        {
            "action_name": "GET_URL",
            "xpaths": [CONFIG_OBJ.get('console_url')],
            "wait_time": 5,
            "keys": None,
            "action_text": "Get INPUT Console Url",
            "no_falsy_value": True
        },
        {
            "action_name": "FIND_ELEMENT_AND_CLICK",
            "xpaths": ["//td[@class='csspage' and contains(text(),'gameslist .csv')]"],
            "wait_time": 5,
            "keys": None,
            "action_text": "Get All Games List For THis  Console",
            "no_falsy_value": True
        }]
    for action_obj in start_actions:
        logger.debug('{}:- {}'.format(action_obj.get('action_name'), action_obj.get('action_text')))
        value = ae_obj.actions(action_obj)
        if not value and action_obj.get('no_falsy_value', False):
            logger.error(
                '{}--{}--{}'.format(action_obj.get('action_name'), action_obj.get('action_text'), 'VALUE REQUIRED'))
            driver.quit()
            exit()

    wait_try = 1
    game_list_downloaded = False
    while (wait_try <= 3):
        if path.exists('gameslist.csv'):
            game_list_downloaded = True
            break
        wait_try += 1
        time.sleep(wait_try + 3)

    if game_list_downloaded:
        import pandas as pd
        df = pd.read_csv('gameslist.csv', delimiter=';')
        game_ids = df['Game ID'].to_list()
        game_names = df['Game Name'].to_list()
    else:
        logger.error("No Games List Found for this console")
        exit()

    FINAL_RESULT_LIST = []
    logger.info("TOTAL GAMES FOR THIS CONSOLE - {}".format(len(game_ids)))
    for game in range(len(game_ids)):

        game_id = game_ids[game]
        game_name = game_names[game]
        if db_obj:
            if db_obj.check_into_db(game_id):
                logger.debug("Game Media Already Donwloaded For -{}".format(game_name))
                continue
        logger.info('Game Id- {}, Game Name- {}'.format(game_id, game_name.upper()))
        RESULT_OBJ = {}
        uu = "https://screenscraper.fr/gameinfos.php?gameid={}&action=onglet&zone=gameinfosinfos".format(game_id)
        ACTIONS_LIST[0]['xpaths'][0] = uu
        for action_obj in ACTIONS_LIST:
            logger.debug('{}:- {}'.format(action_obj.get('action_name'), action_obj.get('action_text')))

            value = ae_obj.actions(action_obj)
            if action_obj.get('source') in ['Video']:
                if type(value) == list:
                    for val in value:
                        if "video-normalized" in val:
                            value = val
                            break
                if type(value) == list:
                    value = value[0]
            if not value and action_obj.get('no_falsy_value', False):
                logger.error(
                    '{}  {}, {}'.format(action_obj.get('action_name'), action_obj.get('action_text'), 'VALUE REQUIRED'))
                driver.quit()
                exit()
            if action_obj.get('source'):
                RESULT_OBJ[action_obj.get('source')] = value

        FINAL_RESULT_OBJ = {}
        '''Naming Convention'''
        platform_name = RESULT_OBJ.get('Platform', 'default')
        platform_name = '_'.join(platform_name.split())
        game_site_name = RESULT_OBJ.get('Game_Name', 'default_name')
        game_site_name = '_'.join(game_site_name.split())
        game_site_name = re.sub('[^A-Za-z0-9._-]', '', game_site_name)
        file_separator = CONFIG_OBJ.get('file_name_separator', '___-___')
        game_site_id = RESULT_OBJ.get('Game_Site_Id', 'default_id')
        folder_name = CONFIG_OBJ['folder_to_save']

        for key in RESULT_OBJ:
            if key in ['Platform', 'Game_Name', 'Number_Of_Players', 'Release_Date', 'Synopsis', 'Game_Site_Id']:
                FINAL_RESULT_OBJ[key] = RESULT_OBJ.get(key, None)
                continue
            asset_media_name = key
            extension = '.jpg'
            if key in ['Video']:
                extension = '.mp4'

            if type(RESULT_OBJ.get(key, [])) == list:
                if len(RESULT_OBJ.get(key, [])) > 0:
                    counter = 1
                    for key__ in RESULT_OBJ.get(key, []):
                        if key__ and ('http' in key__):

                            file_name = '{}/{}{}{}{}{}{}{}_{}{}'.format(folder_name, platform_name,
                                                                        file_separator,
                                                                        game_site_id,
                                                                        file_separator,
                                                                        game_site_name,
                                                                        file_separator,
                                                                        asset_media_name,
                                                                        counter,
                                                                        extension)

                            request_options = {
                                'type': 'GET',
                                'url': key__,
                                'file_name': file_name,
                                'headers': {}
                            }
                            status_code = ae_obj.make_request(request_options)
                            if status_code == 200:
                                FINAL_RESULT_OBJ['{}_{}'.format(key, counter)] = file_name
                                counter += 1
            else:
                file_name = '{}/{}{}{}{}{}{}{}{}'.format(folder_name, platform_name,
                                                         file_separator,
                                                         game_site_id,
                                                         file_separator,
                                                         game_site_name,
                                                         file_separator,
                                                         asset_media_name,
                                                         extension)

                if path.exists(file_name):
                    continue

                request_options = {
                    'type': 'GET',
                    'url': RESULT_OBJ.get(key),
                    'file_name': file_name,
                    'headers': {}
                }
                status_code = ae_obj.make_request(request_options)
                if status_code == 200:
                    FINAL_RESULT_OBJ[key] = file_name

            if key in ['Video']:
                if path.exists(file_name):
                    meta_title = 'Title: {}\nPlatform: {}\nPlayers: {}\nRelease Dates: {}\nSynopsis: {}'.format(
                        FINAL_RESULT_OBJ.get('Game_Name', 'Default'),
                        FINAL_RESULT_OBJ.get('Platform', 'Default'),
                        FINAL_RESULT_OBJ.get('Number_Of_Players', 'Default'),
                        FINAL_RESULT_OBJ.get('Release_Date', 'Default'),
                        FINAL_RESULT_OBJ.get('Synopsis', 'Default')
                    )
                    vp_obj.post_process(file_name, meta_title)
        FINAL_RESULT_LIST.append(FINAL_RESULT_OBJ)
        if db_obj:
            db_obj.write_into_db(game_id)
        logger.info("Done! Game Id {} \n".format(game_id))

    driver.quit()


def create_files_folders(CONFIG_OBJ):
    '''
    :param CONFIG_OBJ: It reads folder_to_save key from the config object, the media downloaded will be saved at this path
                       If there is no folder name mentioned in config, then default folder name is chosen (Media_Download_Folder)
    :return: None
    '''
    if not CONFIG_OBJ.get('folder_to_save'):
        CONFIG_OBJ['folder_to_save'] = 'Media_Download_Folder'
    if not path.exists(CONFIG_OBJ['folder_to_save']):
        os.mkdir('Media_Download_Folder')


if __name__ == '__main__':
    CONFIG_OBJ = {}
    ACTIONS_LIST = []

    logger = Logger.getLogger("Movie_py")
    parser = ConfigParser()
    parser.read('Config')
    params = parser.items('CONFIG_SECTION')
    for param in params:
        CONFIG_OBJ[param[0]] = param[1]
        if param[1].lower() in ["true"]:
            CONFIG_OBJ[param[0]] = True
        elif param[1].lower() in ["false"]:
            CONFIG_OBJ[param[0]] = False
    logger.debug("Config Object Loaded")
    logger.debug(CONFIG_OBJ)

    with open('Action_Steps.json', 'r') as d:
        ACTIONS_LIST = json.load(d)
    logger.debug("Action List Ready - {} Actions".format(len(ACTIONS_LIST)))

    create_files_folders(CONFIG_OBJ)
    driver = get_mozilla_with_extension_enabled()
    if not driver:
        logger.error("Driver Not Loaded -Exit")
        exit()
    logger.info("CONSOLE URL -- {}".format(CONFIG_OBJ.get('console_url')))
    main(driver, ACTIONS_LIST)