# Funcionalidades Extras Trabalho 3 - Chat Em Tempo Real
## Apresentação do projeto 

Este é uma api de chat simples com uma funcionalidade de tradução implementada e uma 
funcionalidade de reação a mensagens. 
O aplicativo permite que os usuários enviem mensagens de texto, editem,enviem mensagens privadas entre eles, e possam excluir asmensagens e fazer upload de ficheiros. 
Além disso, possui a capacidade de traduzir todas as mensagens para o inglês e também aplicar 
reações às mensagens com um único clique sendo as opções de reação like ou deslike.

### Reação a Mensagens
Os botões de reação, são representados por dois icons de like e deslike,assim os usuários podem obtar pelo que acham mais adequado
cada clique no icon faz com que uma mensagem seja exibida do lado de quem envio a mensagem essa mensagem contem o nome do utilizador que reagiu a mensagem e a descrição se gostou ou não da mensagem bem como a cor dependendo do que foi a escolha da reação.


 **Motivo da escolha:**
 - Analise do conteudo
	Com as reação implementadas o utilizador pode ter um sentido mais critico em relação as mensagens que são enviadas no chat, com isso pode expressar a sua opinião de uma forma diferente mais para a frente poderia-se implementar uma funcionalidade que podesse fazer uma sondagem acerca dos utilizadores com mais mensagens de deslike e entender o motivo.
   
 - Interação:
	Com os ícones de reação no chat, os utilizadores têm uma maneira rápida e visualmente intuitiva de expressar  emoções e opiniões sobre as mensagens. Isso promove uma atmosfera mais interativa no chat.Além disso, os ícones de reação podem ajudar a facilitar a comunicação não verbal, adicionando assim uma camada extra de expressão às interações online.

 **Informações detalhadas:**
 
  **Feedback Visual:**
  	Assim que o utilizador clica em um icon de reação uma mensagem no utilizaodr que envio a mensagem é exibida com a informação de quem foi o utilizador que reagiu a mensagem assim como qual foi a sua reação se positiva se negativa ,outra caractristica visual é que quando o utilizador que envio a mensagem tenta reagir a mensagem nada acontece pois é feita uma verificação acerca do id do utilizador 


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
