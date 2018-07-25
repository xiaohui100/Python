"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : Example3.py
 @Time    : 2018/7/24 16:02
"""
import frida


def MessageHandle(message, payload):
    if message["type"] == "error":
        print("[*]Message: ")
        for key, value in message.items():
            print(key, ":", value)
    else:
        print("[*]Message: ", message)
        print("[*]Payload: ", payload)


device = frida.get_usb_device()
pid = device.spawn("com.example.a11x256.frida_test")
session = device.attach(pid)
device.resume(pid)

with open("Example3.js", "r", encoding="utf-8") as f:
    script = session.create_script(f.read())

script.on("message", MessageHandle)  # 添加返回错误的回调显示函数
script.load()

command = ""
while 1 == 1:
    command = input("Enter command:\n1: Exit\n2: Call secret function\nchoice:")
    if command == "1":
        break
    elif command == "2":
        script.exports.callSecretFunction()

