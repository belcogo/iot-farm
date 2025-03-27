Alunos: Bel Cogo, Bruno Hoffmann e João Vítor Accorsi.
Disciplina: Internet das Coisas: Sensores, Protocolos e Aplicações.

# Trabalho de IOT - Farm

## Relatório

## Circuito

## Como rodar o back-end

### Rodando pela primeira vez

1. Rode o `docker-compose up -d` na pasta `src`.
2. Após subir o container do mongo, rode o seeder.py com o intuito de adicionar as coleções ao banco. Comando: `python src/configure_db.py`
3. Rode o `python src/consumer.py` para rodar o consumidor.
4. Rode o `streamlit run main.py` para rodar o front-end.
