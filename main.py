import flet as ft
import uuid

class Message():
    def __init__(self, message_id,user_id,user_name, text, message_type):
        self.message_id = message_id
        self.user_id = user_id
        self.user_name = str(user_name)
        self.text = str(text)
        self.message_type = str(message_type)

class ChatMessage(ft.Row):
    def __init__(self, message: Message,):
        super().__init__() 
        self.message = message
        
        self.edit_msg = ft.TextField(expand=1)
        
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
            ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update",
                    on_click=self.edit_message,
                    visible=False
            ),
            ft.IconButton(
                icon=ft.icons.EDIT,
                tooltip="Edit message",
                on_click=self.edit_message
            ),
            ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Delete message",
                on_click=self.delete_message
            ),
            ft.IconButton(
                icon=ft.icons.DONE_OUTLINE_OUTLINED,
                icon_color=ft.colors.GREEN,
                tooltip="Save",
                on_click=self.save_message,
                visible=False
            ),
        ]
    
    def get_initials(self, user_name):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  

    def get_avatar_color(self, user_name):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
    
    def save_message(self,e):
        pass
    
    def edit_message(self,e):
        print("ola")
        
    def delete_message(self, e):
        user_id = self.page.session.get("user_id")
        #print("user_id",user_id)
        #print("message.user_id",self.message.user_id)
        
        #Comparar o id do usuario que envio a mensagem com o id do usuario de inicio de sessão
        if self.message.user_id == user_id:
            
            # Cria uma mensagem de exclusão para enviar aos outros usuários
            delete_message = Message(message_id=self.message.message_id,user_id=self.message.user_id, user_name=self.message.user_name, text="This message has been deleted.", message_type="delete_message")
            
            # Envia a mensagem de exclusão para todos os usuários
            self.page.pubsub.send_all(delete_message)
            self.update()
    
def main(page):
    
    page.title = "Chat - TP3"  

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            user_id = str(uuid.uuid4())  # Gerar um identificador único para o usuário
            page.session.set("user_id", user_id)
            page.session.set("user_name", join_user_name.value)
            
            page.dialog.open = False
            
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(message_id=str(uuid.uuid4()),user_id=user_id,user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            user_id = page.session.get("user_id")
            user_name = page.session.get("user_name")
            
            # Gera um ID único para a mensagem
            message_id = str(uuid.uuid4())
            
            page.pubsub.send_all(Message(message_id=message_id,user_id=user_id, user_name=user_name, text=new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        m  = None 
        if message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE54, size=12)
        elif message.message_type == "delete_message":
            # Verifica se a mensagem de exclusão é do usuário atual
            for control in chat.controls:
                if isinstance(control, ChatMessage) and control.message.message_id == message.message_id:
                    chat.controls.remove(control)
                    m = ft.Text(f"{message.user_name}'s message has been deleted.")
        else:
            m = ChatMessage(message)
            
        if m is not None:
            chat.controls.append(m)
            page.update()
            
    page.pubsub.subscribe(on_message)

    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    page.add(
        ft.Row(
            [ft.Text(value=" \n Bem vindo ao Chat 👋 \n ", style="headlineMedium",color="white")],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

if __name__ == "__main__":
    ft.app(target=main, 
            assets_dir="assets",
            view=ft.WEB_BROWSER,
            port=8550)
