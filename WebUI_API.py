from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class WebUI_CONTROL:
    def access_to_webui(self):
        driver_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=driver_service)
        try:
            self.driver.get("http://127.0.0.1:7860")
        except:
            return 'can not access error'
        
        time.sleep(2)          
        
        buffer_element = self.driver.find_element(By.CSS_SELECTOR, 'body > gradio-app').shadow_root
        self.main_element = buffer_element.find_element(By.CSS_SELECTOR, 'div.gradio-container.dark > div.w-full.flex.flex-col.min-h-screen > div')
        return 'success'

    def input_prompt(self, prompt):
        """ プロンプトを変更 

        Args:
            prompt(str): プロンプト
        """
        prompt_textarea = self.main_element.find_elements(By.TAG_NAME, 'textarea')[0]
        prompt_textarea.clear()
        prompt_textarea.send_keys(prompt)
        time.sleep(0.5)

    def input_negative_prompt(self, prompt):
        """ ネガティブプロンプトを変更

        Args:
            prompt(str): ネガティブプロンプト
        """
        prompt_textarea = self.main_element.find_elements(By.TAG_NAME, 'textarea')[1]
        prompt_textarea.clear()
        prompt_textarea.send_keys(prompt)
        time.sleep(0.5)

    def input_steps(self, steps):
        """ ステップ数を変更
        """
        steps_box = self.main_element.find_elements(By.TAG_NAME, 'input')[2]
        steps_box.clear()
        steps_box.send_keys(steps)

    def generate(self):
        """ Do Generate
        """
        time.sleep(1)
        self.main_element.find_element(By.ID, 'txt2img_generate_box').click()

    def get_models(self):
        """ モデルのリストが返ってくるやで

        return:
            models_list(list): モデルのリスト
        """
        models_elem = self.main_element.find_element(By.ID, 'setting_sd_model_checkpoint')
        models_list = models_elem.text.split('\n')
        return models_list
    
    def get_progress(self):
        """ 進捗具合

        return:
            進捗具合: finished or percent
        """
        if len(self.main_element.find_elements(By.CLASS_NAME, 'progressDiv')) != 0:
            return self.main_element.find_element(By.CLASS_NAME, 'progressDiv').text
        else:
            return 'finished'

if __name__ == "__main__":
    webui = WebUI_CONTROL()
    if webui.access_to_webui() == 'success':
        webui.input_prompt('Nekopara fantastically detailed eyes modern anime style art cute vibrant detailed ears girl nekomimi dress portrait shinkai makoto studio ghibli sakimichan stanley artgerm lau rossdraws james jean marc simonetti elegant highly detailed digital painting artstation pixiv')
        webui.input_steps(5)
        print(webui.get_progress())
        webui.generate()
        time.sleep(5)
        print(webui.get_progress())

    else:
        print('サイトにアクセスできません')