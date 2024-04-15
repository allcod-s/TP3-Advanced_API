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
    def __init__(self, message: Message):
        super().__init__() 
        self.message = message
        
        self.edit_msg = ft.TextField(visible=False)
    
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    #ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
            ft.IconButton(
                icon=ft.icons.EDIT,
                tooltip="Edit message",
                on_click=self.edit_message,
            ),
            ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Delete message",
                on_click=self.delete_message
            ),
            self.edit_msg,
            ft.IconButton(
                icon=ft.icons.DONE_OUTLINE_OUTLINED,
                icon_color=ft.colors.GREEN,
                tooltip="Update",
                on_click=self.save_message,
                visible=False
            ),
        ]
    
    def get_initials(self, user_name):
        if user_name:
            return user_name[:2].capitalize()
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
    
    def edit_message(self,e):
        user_id = self.page.session.get("user_id")
        
        self.edit_msg.value = self.message.text  # Preenche o campo de edição com o texto atual da mensagem
        #print("edit_msg.value",self.edit_msg.value)
        
        if self.message.user_id == user_id:
            for i,control in enumerate(self.controls):
                if isinstance(control, ft.IconButton) and control.icon in [ft.icons.EDIT,ft.icons.DELETE]:
                    control.visible = False  # Esconde o botão de edição

                elif isinstance(control, ft.IconButton) and control.icon == ft.icons.DONE_OUTLINE_OUTLINED:
                    control.visible = True  # Mostra o botão "done"
                    self.edit_msg.visible = True
        
                #Verifica se é se esta no ft.Colum 
                elif isinstance(control, ft.Column) and  i == 1: #acede ao control na segunda posição
                    control.visible = False
                    
        self.update()
 
    def save_message(self, e):
        user_id = self.page.session.get("user_id")
        
        if self.message.user_id == user_id:
            self.message.text = self.edit_msg.value
            
            self.update()
            
            # Cria uma nova mensagem editada
            edited_message = Message(message_id=self.message.message_id, user_id=user_id, 
                                     user_name=self.message.user_name, text=self.edit_msg.value, 
                                     message_type="edit_message")
            
            # Envia a nova mensagem editada para todas as sessões
            self.page.pubsub.send_all(edited_message)
            
            # Remover a mensagem original
            for control in self.controls:
                if isinstance(control, ft.Column):
                    self.controls.remove(control)
                    break
            
            # Criar uma nova instância de ChatMessage com o texto atualizado
            updated_message = ChatMessage(self.message)
            
            # Adicionar a nova mensagem à lista de controles
            self.controls.insert(1, updated_message)
            
            # Atualizar a interface do usuário
            for control in self.controls:
                if isinstance(control, ft.IconButton) and control.icon in [ft.icons.EDIT, ft.icons.DELETE]:
                    control.visible = False
                elif isinstance(control, ft.IconButton) and control.icon == ft.icons.DONE_OUTLINE_OUTLINED:
                    control.visible = False
                    self.edit_msg.visible = False
                elif isinstance(control,ft.CircleAvatar) and control.content != "":
                    control.visible = False
    
        self.update()
        
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
        elif message.message_type == "edit_message":
            for control in chat.controls:
                if isinstance(control, ChatMessage) and control.message.message_id == message.message_id:
                    for sub_control in control.controls:
                        if isinstance(sub_control, ft.Column):
                            for text_control in sub_control.controls:
                                if isinstance(text_control, ft.Text):
                                    text_control.value = message.text
                                    m = ft.Text(f"{message.user_name}'s message has been edited.")
                    control.update()
                    
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
