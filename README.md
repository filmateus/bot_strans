Em 2022, a strans adotou um novo sistema de gestão de autos de trânsito com o objetivo de solucionar os problemas recorrentes que o sistema até então utilizado possuia. O novo sistema, para administração, foi uma boa decisão, para a análises de dados, nem tanto.

Com o antigo sistema era possível acessar o banco de dados em formato SQL e realizar consultas e análises. Com o novo sistema, não havia acesso ao banco de dados, pois o sistema era mais restristo.

Foi preciso pensar em soluções para contornar o problema de acesso aos dados e assim continuar o trabalho.

A solução adotada incluiu utilizar automatização para capturar algumas informações via web scraping utilizando pacote selenium com linguagem python e para armazenar as informações foi criado um banco de dados em SQL e tabelas.

Dois arquivos foram criados. O primeiro, em jupyter notebook, para amazenar os autos já registrados durante o período sem a criação do banco de dados. Nesse processo, ainda precisaríamos disponilizar um arquivo xlsx com  os autos que deveriam ser consultados e salvos. 

No segundo arquivo, em formato py, o processo foi totalmente automatizado para captura dos números dos autos e para pesquisa. 
