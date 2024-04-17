from typing import Dict
import os

import flet as ft
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    Page,
    ProgressRing,
    Ref,
    Row,
    Text,
    icons,
)

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
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
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
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

# Variável global para armazenar as salas de chat
chat_rooms = {
    1: {"name": "private chat", "messages": []},
    2: {"name": "Chat 1", "messages": []},
    3: {"name": "Chat 2", "messages": []},
}

def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Chat"

    # Initialize files as a Column
    files = Column()

    prog_bars: Dict[str, ProgressRing] = {}
    upload_button = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent, new_message_field: ft.TextField):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.controls.clear()  # Now you can safely clear controls
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.controls.append(Row([prog, Text(f.name)]))
                # Update the new_message field with the selected file name
                new_message_field.value += f.name + " "
        page.update()

    file_picker = FilePicker(on_result=lambda e: file_picker_result(e, new_message))

    def upload_files(e):
        upload_list = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                upload_list.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(upload_list)

    ft.ElevatedButton("Upload", on_click=upload_files)

    # hide dialog in an overlay
    page.overlay.append(file_picker)

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def send_chat_update():
        page.pubsub.send_all(Message(user_name="System", text="New chat room created", message_type="chat_update"))

    def close_dlg_confirm(e):
        chat_name_field = dlg_modal.actions[0]  # O primeiro elemento das ações é o campo de texto
        if chat_name_field.value:
            chat_name = chat_name_field.value
            # Gere um ID único para a sala de chat (pode ser simplesmente o número de salas criadas até agora)
            chat_id = len(chat_rooms) + 1
            # Adicione a nova sala ao dicionário
            chat_rooms[chat_id] = {"name": chat_name, "messages": []}  # Adicione mais detalhes conforme necessário
            # Print para verificar se a sala foi criada com sucesso
            print("Sala de chat adicionada com sucesso:")
            print(chat_rooms[chat_id])
            # Atualize a lista de salas de chat
            room_list.controls.clear()
            room_list.controls.extend([
                ft.ElevatedButton(f"{room_id}: {chat_rooms[room_id]['name']}", on_click=lambda e, room_id=room_id: join_room(room_id))
                for room_id in chat_rooms
            ])
            # Envie uma mensagem de atualização para todos os clientes conectados
            send_chat_update()  # Enviar mensagem de atualização
        dlg_modal.actions[0].value = ""  # Limpa o valor do campo de texto
        dlg_modal.open = False
        page.update()

    def close_dlg_cancel(e):
        dlg_modal.actions[0].value = ""  # Limpa o valor do campo de texto
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Create Chat Room"),
        actions=[
            ft.TextField(label="Enter your chat name"),
            ft.Text("", height=10),  # Empty text for spacing
            Row([
                ft.ElevatedButton("Confirm", on_click=close_dlg_confirm),
                ft.ElevatedButton("Cancel", on_click=close_dlg_cancel),
            ]),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def create_chat_room_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def send_message_click(e):
        if new_message.value != "":
            active_room_id = page.session.get("active_room")
            if active_room_id is not None:
                message = Message(page.session.get("user_name"), new_message.value, message_type="chat_message")
                chat_rooms[active_room_id]["messages"].append(message)
                page.pubsub.send_all(message)  # Envia a mensagem para todas as sessões conectadas
            else:
                print("No active room selected!")
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        m = None  # Definir m como None inicialmente
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        elif message.message_type == "chat_update":
            # Atualize a lista de salas de chat
            room_list.controls.clear()
            room_list.controls.extend([
                ft.ElevatedButton(f"{room_id}: {chat_rooms[room_id]['name']}", on_click=lambda e, room_id=room_id: join_room(room_id))
                for room_id in chat_rooms
            ])
        if m is not None:  # Verificar se m foi definido antes de adicionar
            chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def join_room(room_id):
        active_room = chat_rooms.get(room_id)
        if active_room:
            page.session.set("active_room", room_id)
            chat.controls.clear()
            for message in active_room["messages"]:
                chat.controls.append(ChatMessage(message))
        else:
            # Sala de chat não encontrada ou erro
            pass
        page.update()

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

    room_list = ft.ListView(
        expand=False,
        spacing=10,
    )

    room_list.controls = [
        ft.ElevatedButton(f"{room_id}: {chat_rooms[room_id]['name']}", on_click=lambda e, room_id=room_id: join_room(room_id))
        for room_id in chat_rooms
    ]

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
                    icon=ft.icons.ADD_CIRCLE_OUTLINE,
                    tooltip="Create Chat Room",
                    on_click=create_chat_room_modal
                ),
                ft.IconButton(
                    icon=ft.icons.UPLOAD,
                    tooltip="Choose File",
                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                ),
                ElevatedButton(
                    "Upload",
                    ref=upload_button,
                    icon=icons.UPLOAD,
                    on_click=upload_files,
                    disabled=True,
                ),
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ],
        ),
    )
    page.add(room_list)

# Setting FLET_SECRET_KEY
os.environ["FLET_SECRET_KEY"] = "4ebe2bae5b15a50d4a7f2629a240ba30edf91724948fbeea7c53a89b1d127e8d"

ft.app(port=8550, target=main, view=ft.WEB_BROWSER, assets_dir="assets", upload_dir="assets/uploads")
