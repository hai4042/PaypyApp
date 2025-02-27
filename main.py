from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import requests
import hashlib

class PaypyApp(App):
    def build(self):
        self.api_domain = "https://www.xiazyba.com"
        self.api_path = "/wp-content/plugins/paypy/notify.php"
        self.secret_key = "wq355tfvfd3542680"
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 订单信息输入
        self.order_id_input = TextInput(hint_text='输入订单号')
        self.price_input = TextInput(hint_text='输入金额（如：10.00）')
        self.type_input = TextInput(hint_text='支付类型（alipay/wechat）')
        
        # 补单按钮
        btn_retry = Button(text='手动补单', size_hint=(1, 0.2))
        btn_retry.bind(on_press=self.manual_retry)
        
        layout.add_widget(Label(text='Paypy补单工具'))
        layout.add_widget(self.order_id_input)
        layout.add_widget(self.price_input)
        layout.add_widget(self.type_input)
        layout.add_widget(btn_retry)
        
        return layout

    def generate_sign(self, price, order_type):
        # 生成签名（与插件逻辑一致）
        md5_str = hashlib.md5(f"{price}{order_type}".encode()).hexdigest()
        full_str = md5_str + self.secret_key + "paypy"
        return hashlib.md5(full_str.encode()).hexdigest()

    def manual_retry(self, instance):
        order_id = self.order_id_input.text
        price = self.price_input.text
        order_type = self.type_input.text
        
        if not all([order_id, price, order_type]):
            self.show_popup("错误", "请填写所有字段")
            return
        
        try:
            # 构造请求参数
            params = {
                'sign': self.generate_sign(price, order_type),
                'price': price,
                'type': order_type,
                'plugin': 'paypy'
            }
            
            # 发送GET请求
            url = f"{self.api_domain}{self.api_path}"
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 1:
                    self.show_popup("成功", "补单成功！")
                else:
                    self.show_popup("失败", result.get('msg', '未知错误'))
            else:
                self.show_popup("错误", f"服务器响应异常：{response.status_code}")
        
        except Exception as e:
            self.show_popup("错误", f"网络请求失败：{str(e)}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        btn = Button(text='关闭', size_hint=(1, 0.4))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    PaypyApp().run()