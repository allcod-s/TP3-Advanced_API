# API avançada 
import flet as ft 

def main(page):
    
	page.title = "Chat - TP3"
	page.window_width = 500
	page.window_height = 600
	
	chat = ft.Column()
	new_message = ft.TextField()

	def send_click(e):
		chat.controls.append(ft.Text(new_message.value))
		new_message.value = ""
		page.update()
  
	page.add(
     	ft.Row(
			[ft.Text(value=" \n Chat ", style="headlineMedium",color="White")],
			alignment=ft.MainAxisAlignment.CENTER,
			),
			#CallCalculator(page)
		chat, ft.Row(
      		controls=[new_message, ft.ElevatedButton("Enviar", on_click=send_click)]
        )
	)

if __name__ == "__main__":
	ft.app(target=main,assets_dir="assets",view=ft.AppView.WEB_BROWSER)
