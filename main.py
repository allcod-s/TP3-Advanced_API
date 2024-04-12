import flet as ft

class Message():
    def __init__(self, user_name ,text, message_type):
        self.user_name = str(user_name)
        self.text = str(text)
        self.message_type = str(message_type)
        self.id = id(self) # Adicionar um identificador a mensagem

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__() # Vai buscar a class Row antes de iniciar a ChatMessage
        self.message = message # Guarda a mensgaem 
        self.vertical_alignment ="start"
        self.controls=[
                ft.CircleAvatar( #Criar o avatar com o nome do usar e o formato
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
                    spacing=5, #Espaço entre o nome e o texto
                ),
                ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        tooltip="Edit message",
                        on_click=self.edit_message
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        tooltip="Delete message",
                        on_click=self.delete_message(message.id)
                    ),      
                ],
            ),
        ]

    def get_initials(self, user_name):
        if user_name:
            return user_name[:1].capitalize() #Coloca apenas a primeira letra como miuscula
        else:
            return "Unknown"  

    def get_avatar_color(self, user_name): #Define as cores do avatar
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
        return colors_lookup[hash(user_name) % len(colors_lookup)] #Ver esta linha 
        
    def edit_message(self):   
        pass
    
    def delete_message(self,message_id):
        pass
    
def main(page):
    page.title = "Chat - TP3"  

    def join_chat_click(e):
        #Se não colocarmos nenhum user name
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            
            #Adiciona o prefix antes de escrever 
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            
            #Ver a caor de texto---
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "": # Se não existir nenhuma mensagem para enviar 
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            new_message.value = "" # Depois volta a vazio
            new_message.focus() # Continuar com o campo selecionado
            page.update()

    def on_message(message: Message):  #Edita o meu message_type
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE54, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
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

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
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

    # Add everything to the page
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
 