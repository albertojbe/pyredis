# 🧠 Redis Clone em Python

Este projeto é uma implementação simplificada de um servidor Redis em Python, utilizando o protocolo RESP. O objetivo é demonstrar como o Redis funciona internamente, incluindo o processamento de comandos, armazenamento de dados na memória e gerenciamento de conexões por socket.

---

## 📌 O que é o Redis?

**Redis** (REmote DIctionary Server) é uma estrutura de armazenamento de dados em memória, do tipo chave-valor, extremamente rápida e usada para caching, filas, contadores, entre outros. Ele é conhecido por sua simplicidade, performance e suporte a diversos tipos de dados, como strings, listas, sets e hashes.

Além disso, o Redis suporta persistência opcional em disco e pode atuar como um banco de dados NoSQL leve.

---

## 🔁 O que é o protocolo RESP?

**RESP** (REdis Serialization Protocol) é o protocolo de comunicação utilizado pelo Redis. Ele é simples, eficiente e permite representar diferentes tipos de dados de forma textual.

### Exemplos de comandos em RESP:
- `PING` → `*1\r\n$4\r\nPING\r\n`
- `SET key value` → `*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n`

Esse projeto utiliza uma biblioteca chamada `resp_codec` (presumidamente implementada à parte) para codificar e decodificar mensagens RESP.

---

## 🧩 Estrutura do Projeto

O servidor implementa comandos básicos do Redis, trabalhando com persistência local em JSON e execução concorrente com `threading`.

### 📁 Arquivos:
- `main.py` → Contém a implementação principal do servidor e processamento dos comandos.
- `db.json` → Usado para persistir os dados do armazenamento (`storage`).
- `resp_codec.py` → (Não incluído aqui) Módulo auxiliar responsável por codificação/decodificação RESP.

---

## 🧠 Funcionalidades Implementadas

O servidor escuta conexões na porta `6379` (como o Redis real) e responde a diversos comandos básicos:

### Comandos Suportados:

| Comando     | Descrição                                                    |
|-------------|---------------------------------------------------------------|
| `PING`      | Retorna `PONG`                                                |
| `ECHO msg`  | Retorna a mensagem enviada                                    |
| `SET`       | Armazena um valor com chave opcionalmente expirada           |
| `GET`       | Retorna o valor associado à chave                             |
| `EXISTS`    | Retorna `1` se a chave existir, `0` caso contrário            |
| `DEL`       | Remove uma ou mais chaves                                     |
| `INCR`      | Incrementa o valor numérico da chave (ou inicializa em 1)     |
| `DECR`      | Decrementa o valor numérico da chave (ou inicializa em 1)     |
| `SAVE`      | Persiste o estado atual do banco no arquivo `db.json`         |
| `CONFIG`    | Retorna uma lista vazia (placeholder)                         |

### ⏱ Suporte a Expiração
Os comandos `SET` suportam as seguintes opções de expiração:
- `EX`: Expiração em segundos.
- `PX`: Expiração em milissegundos.
- `EXAT`: Timestamp absoluto em segundos.
- `PXAT`: Timestamp absoluto em milissegundos.

O servidor verifica a expiração ao acessar as chaves (`GET`).

---

## 🧵 Conexões e Concorrência

O servidor utiliza `socket.create_server` para escutar conexões TCP, e cria uma nova thread (`threading.Thread`) para cada cliente conectado. Cada thread gerencia a comunicação e execução de comandos daquele cliente.

---

## 💾 Persistência

Os dados armazenados em memória (`storage`) são carregados do arquivo `db.json` ao iniciar e podem ser salvos com o comando `SAVE`.

---

## 🚀 Executando o Servidor

1. Execute o servidor:
   ```bash
   python main.py
   ```
2. Use um cliente Redis ou um cliente customizado que envia comandos via RESP para `localhost:6379`.

---