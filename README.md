# Funcionalidades Extras Trabalho 3 - Chat Em Tempo Real
## Apresentação do projeto 

Este é um aplicativo de chat simples com uma funcionalidade de tradução implementada e uma 
funcionalidade de reação a mensagens. 
O aplicativo permite que os usuários enviem mensagens de texto, editem e excluam suas mensagens. 
Além disso, possui a capacidade de traduzir todas as mensagens para o inglês e também aplicar 
reações às mensagenscom um único clique.

### Reação a Mensagens
 

### Tradução de Mensagens
 O botão de tradução, representado por um ícone de tradução, permite que os usuários alternem entre
 mensagens traduzidas em inglês e originais. Cada clique no botão de tradução alterna entre os dois 
 estados.

 **Motivo da escolha:**
 - Facilidade de Compreenção:
      A tradução automática permite que os usuários compreendam o conteúdo do chat em seu idioma nativo,
   		tornando a interação mais fácil e acessível.
   
 - Inclusão Cultural:
			Ao permitir a tradução das mensagens, valorizamos e respeitamos as diferentes origens e idiomas dos nossos usuários.

 **Informações detalhadas:**

 - **Integração com API de Tradução:**
   		Utilizamos uma API de tradução confiável para realizar as traduções de forma rápida e precisa.
   		A integração com essa API garante que as traduções sejam atualizadas e precisas.
   
 - **Feedback Visual:**
			Após clicar no botão de tradução, o texto da mensagem é substituído pela sua tradução no idioma configurado pelo usuário.
   Isso permite uma compreensão imediata do conteúdo da mensagem traduzida.
   
 - **Tradução Bidirecional:**
   Os usuários têm a capacidade de traduzir tanto mensagens recebidas quanto mensagens que desejam enviar. Isso torna o processo de comunicação mais dinâmico e flexível.

			
 

### Tecnologias Utilizadas
**Python:** O backend do aplicativo foi desenvolvido em Python, utilizando a biblioteca FastAPI para a criação da API.
**Google Translate API:** A funcionalidade de tradução é implementada usando a API do Google Translate para traduzir as mensagens para o inglês.
