# 🧸 Rotina Familiar Zen com IA: Seu Assistente Pessoal para Dias Mais Tranquilos 👨‍👩‍👧‍👦

**(Zen Family Routine with AI: Your Personal Assistant for More Peaceful Days)**

---

👋 Olá! Sou o Haroldo, um desenvolvedor colombiano iniciante e pai, construindo com entusiasmo esta solução para um desafio que muitas famílias que trabalham remotamente conhecem bem: como podemos criar uma rotina familiar harmoniosa que apoie o desenvolvimento dos nossos pequenos e, ao mesmo tempo, nos permita ser produtivos?

Este projeto nasceu da minha própria necessidade de trazer mais calma e estrutura para os nossos dias com a nossa filha Zoe, de 2 anos e 8 meses, enquanto minha esposa Liss e eu tocamos nossa startup em casa. Se você também busca uma forma mais inteligente e adaptável de gerenciar o dia a dia da sua família, você está no lugar certo!

This project uses **Google's Agent Development Kit (ADK)** and **Gemini AI Models** to create a multi-agent system designed to help plan and optimize your family's weekly routine. It's built with love, a desire for more quality family time, and a beginner's passion for AI!

## 🌟 O Que Este Sistema Faz? (What Does This System Do?)

Imagine ter uma equipe de assistentes de IA dedicados a facilitar diferentes aspectos da sua rotina familiar:

1.  **🤖 Agente Planejador de Rotina Adaptativa (Adaptive Routine Planner):**
    *   Cria e ajusta dinamicamente a rotina diária da sua criança, considerando a hora que ela acordou, o feedback do dia anterior e o ritmo biológico dela. Chega de tentar encaixar a vida em horários rígidos!
    *   *(Creates and dynamically adjusts your child's daily routine, considering wake-up times, previous day's feedback, and natural rhythms.)*

2.  **🥕 Agente Chef Nutricional (Nutritional Chef Assistant):**
    *   Gera sugestões de cardápios diários para toda a família (sim, para os pais também!), alinhados com os ingredientes que você tem em casa e as necessidades nutricionais dos pequenos.
    *   *(Generates daily meal plan suggestions for the whole family, considering available ingredients and toddler's nutritional needs.)*

3.  **🤸‍♀️ Agente Coordenador de Atividades (Activity Coordinator):**
    *   Sugere atividades criativas e de desenvolvimento para sua criança que não envolvem telas, utilizando recursos que você já tem em casa. Promove autonomia e diversão!
    *   *(Suggests screen-free, developmental activities for your child using home resources, promoting autonomy and fun.)*

4.  **📊 Agente Coach de Progresso (Progress Coach & Evaluator):**
    *   Analisa o feedback semanal e os "logs" da rotina para oferecer insights, identificar padrões, celebrar sucessos e sugerir ajustes para a melhoria contínua – sempre com foco no bem-estar da criança e na preparação para futuras transições (como a ida para a creche).
    *   *(Analyzes weekly feedback and routine logs to offer insights, celebrate successes, and suggest adjustments for continuous improvement.)*

## ✨ Features (Funcionalidades Principais)

*   **🧠 Inteligência Adaptativa:** Os agentes usam modelos Gemini da Google para processar informações e gerar sugestões personalizadas.
*   **🔧 Construído com Google ADK:** Utiliza o Agent Development Kit da Google para a estrutura dos agentes.
*   **🗣️ Saída Multi-Idioma (Multi-Language Output):** Atualmente, os agentes podem fornecer suas sugestões em **Português do Brasil (pt-BR)** e **Espanhol Latino-Americano (es-LA)**. As instruções internas para os agentes estão em Inglês.
*   **👀 Observabilidade (Observability - Opcional):** Integrado com [LangSmith](https://smith.langchain.com/) para rastrear e depurar as execuções dos agentes (requer configuração de API Key da LangSmith).
*   **📝 Código Aberto e Iterativo:** Este é um projeto em evolução, e sua colaboração é bem-vinda!
*   **💻 Ambiente Colab-Friendly:** Projetado para ser facilmente executado e experimentado no Google Colab.

## 🚀 Primeiros Passos (Getting Started)

1.  **Clone este Repositório:**
    ```bash
    git clone https://github.com/HaroldSthid/GeminiADKPracticeCOL.git
    cd [GeminiADKPracticeCOL]
    ```
2.  **Abra no Google Colab:**
    *   Faça o upload do arquivo `.ipynb` principal para o Google Colab.
3.  **Configure suas API Keys (Configure Your API Keys):**
    *   **Google Gemini API Key:**
        *   Obtenha sua chave no [Google AI Studio](https://aistudio.google.com/app/apikey).
        *   No Colab, vá em "Secrets" (ícone de chave na barra lateral esquerda) e adicione um novo segredo chamado `GOOGLE_API_KEY_SECONDARY` (ou o nome que você usou no script) com o valor da sua chave. Certifique-se de que o acesso ao notebook está ativado.
    *   **LangSmith API Key (Opcional, para Observabilidade):**
        *   Crie uma conta e uma API Key (Personal Access Token) no [LangSmith](https://smith.langchain.com/).
        *   No Colab, adicione um segredo chamado `LANGSMITH_API_KEY_FAMILY_PROJECT` (ou o nome que você usou) com o valor da sua chave LangSmith.
        *   Configure as variáveis de ambiente `LANGCHAIN_PROJECT` no script conforme desejar.
4.  **Execute os Passos do Notebook:**
    *   Siga as células do notebook (`.ipynb`) em ordem. O script instalará as dependências (`google-generativeai`, `google-adk`, `langsmith`), configurará os agentes e executará o pipeline.
    *   Você será solicitado a fornecer algumas informações, como o idioma de saída desejado e a que horas seu filho(a) acordou.

## 🛠️ Estrutura do Código (Code Structure Overview)

O notebook está organizado nos seguintes passos principais:

*   **PASSO 1-2:** Instalação das bibliotecas necessárias.
*   **PASSO 3:** Importações de módulos.
*   **PASSO 4:** Configuração das API Keys (Gemini e LangSmith).
*   **PASSO 5:** Configuração de Advertências.
*   **PASSO 6:** Definição de Funções Auxiliares (`call_agent` para executar os agentes e interagir com LangSmith, `to_markdown` para formatar a saída).
*   **PASSO 7:** Definição dos 4 Agentes Principais (`define_routine_planner_agent`, `define_meal_planner_agent`, `define_activity_coordinator_agent`, `define_progress_coach_agent`). É aqui que a "personalidade" e as instruções de cada agente são moldadas!
*   **PASSO 8:** Lógica Principal de Orquestração, onde os agentes são chamados em sequência, passando informações de um para o outro.

## 💡 Hacks de Valor e Ideias para o Futuro (Value Hacks & Future Ideas)

Este projeto é um ponto de partida. Acredito que ele tem um potencial enorme!

*   **Personalização Profunda dos Prompts:** A "mágica" acontece nas `instructions` de cada agente. Experimente, refine e adapte-as à dinâmica única da sua família!
*   **Integração com Calendários:** Conectar o `AgenteRutina` com o Google Calendar ou similar.
*   **Agente Orquestrador Inteligente:** Atualmente, a orquestração é sequencial. Uma versão Pro poderia ter um quinto agente, o "Maestro da Família", que decide dinamicamente qual agente chamar com base em inputs em tempo real ou eventos.
*   **Inputs Mais Ricos:**
    *   Feedback por voz para a mãe.
    *   Lista de compras gerada automaticamente pelo `AgenteAlimentacion` e enviada para um app.
    *   `AgenteAtividades` usando computer vision para "ver" os brinquedos disponíveis (sonho alto!).
*   **Interface Gráfica (UI):** Uma interface web simples com Streamlit ou Gradio para facilitar a interação da família.
*   **Métricas de Bem-Estar:** O `AgenteCoach` poderia incorporar métricas mais objetivas de sono ou atividade (se houver dados de wearables, por exemplo).

## ❤️ Convite à Colaboração (Invitation to Collaborate)

Como mencionei, sou um desenvolvedor iniciante da Colômbia 🇨🇴, e este projeto é um trabalho de amor e aprendizado. Adoraria ver esta ideia crescer e se tornar ainda mais útil para outras famílias.

Se você tem ideias, sugestões, encontrou um bug, ou quer contribuir com código:

*   Abra uma **Issue** para discutir suas ideias ou reportar problemas.
*   Crie um **Pull Request** com suas melhorias.
*   Compartilhe como você adaptou o sistema para a sua família!

Vamos juntos construir ferramentas que realmente façam a diferença no nosso dia a dia. Mesmo pequenos ajustes nos prompts ou novas ideias para os agentes são contribuições valiosísimas!

---
