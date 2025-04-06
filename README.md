# Trabalho de IOT - Farm

Alunos: Bel Cogo, Bruno Hoffmann e João Vítor Accorsi. <br />
Disciplina: Internet das Coisas: Sensores, Protocolos e Aplicações.

## Objetivo

Este trabalho simula o controle de uma plantação em uma fazenda a partir do uso de IoT. No local da planatação, a partir do uso de sensores, é feita a coleta de dados de temperatura, humidade e luminosidade; assim, os dados são publicados no tópico `/sensor-iot-unisinos-send`, e processados por um cliente. O cliente os armazena em um banco MongoDB, e consegue vizualizar o histórico através do `Streamlit`. Dessa forma, quando uma das grandezas sai fora de um limite pré-estabelecido, um tópico publicado em `/sensor-iot-unisinos-receive` sinaliza isso, e um led é acesso, representando uma ação na fazenda.

## Circuito Wokwi
Link: https://wokwi.com/projects/425992694227693569

![image](https://github.com/user-attachments/assets/8a58eee0-ce69-46db-9245-dbde38379b31)

### Rodando pela primeira vez

1. Rode o `docker-compose up -d` na pasta `src`. <br />
2. Após subir o container do mongo, rode o seeder.py com o intuito de adicionar as coleções ao banco. Comando: `python src/configure_db.py`. <br />
3. Rode o `python src/consumer.py` para rodar o consumidor. <br />
4. Rode o `streamlit run main.py` para rodar o front-end. <br />

### Streamlit

A partir do uso do `Streamlit`, uma biblioteca do Python, é possível vizualizar os dados em tempo real na web acessando http://localhost:8501.

![image](https://github.com/user-attachments/assets/821ffa2f-d8b8-4118-9ca6-e51e93b580bd)

![image](https://github.com/user-attachments/assets/aec2c684-b9ea-4553-bc77-150e44506269)

### Tecnologias/Hardware Utilizado

- ESP32 (ADC)
- LDR
- DHT22
- Python
- Streamlit
- Docker
- MongoDB
