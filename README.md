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

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HaroldSthid/GeminiADKPracticeCOL/blob/main/NOME_DO_SEU_NOTEBOOK_AQUI.ipynb) 
<!-- ^^^ SUBSTITUA 'NOME_DO_SEU_NOTEBOOK_AQUI.ipynb' PELO NOME REAL DO SEU ARQUIVO .ipynb ^^^ -->
<!-- E garanta que a branch é 'main' ou a correta (ex: main, master) -->

1.  **Clonar este Repositório:**
    ```bash
    git clone https://github.com/HaroldSthid/GeminiADKPracticeCOL.git
    cd GeminiADKPracticeCOL
    ```
2.  **Abra no Google Colab:**
    *   Você pode clicar no botão "Abrir no Colab" acima (depois de substituir o nome do notebook no link).
    *   Ou, após clonar o repositório, faça o upload do arquivo `.ipynb` principal do projeto (que você colocou no repositório) para o Google Colab.
3.  **Configure suas API Keys (Configure Your API Keys):**
    *   **Google Gemini API Key:**
        *   Obtenha sua chave no [Google AI Studio](https://aistudio.google.com/app/apikey).
        *   No Colab, vá em "Secrets" (ícone de chave na barra lateral esquerda) e adicione um novo segredo chamado `GOOGLE_API_KEY_SECONDARY` (ou o nome exato que você usou no script, como `GOOGLE_API_KEY` se preferir) com o valor da sua chave. Certifique-se de que o acesso ao notebook está ativado para este segredo.
    *   **LangSmith API Key (Opcional, para Observabilidade):**
        *   Crie uma conta e uma API Key (Personal Access Token) no [LangSmith](https://smith.langchain.com/).
        *   No Colab, adicione um segredo chamado `LANGSMITH_API_KEY_FAMILY_PROJECT` (ou o nome exato que você usou no script) com o valor da sua chave LangSmith. Ative o acesso ao notebook para este segredo.
        *   Configure a variável de ambiente `LANGCHAIN_PROJECT` no script com o nome do projeto que você deseja ver no LangSmith (ex: `ADK_Family_Routine_Optimizer_V1`).
4.  **Execute os Passos do Notebook:**
    *   Siga as células do notebook (`.ipynb`) em ordem. O script instalará as dependências (`google-generativeai`, `google-adk`, `langsmith`), configurará os agentes e executará o pipeline.
    *   Você será solicitado a fornecer algumas informações, como o idioma de saída desejado e a que horas seu filho(a) acordou.

## 🛠️ Estrutura do Código (Code Structure Overview)

O notebook (`.ipynb`) está organizado nos seguintes passos principais:

*   **PASSO 1-2:** Instalação das bibliotecas necessárias.
*   **PASSO 3:** Importações de módulos.
*   **PASSO 4:** Configuração das API Keys (Gemini e LangSmith).
*   **PASSO 5:** Configuração de Advertências.
*   **PASSO 6:** Definição de Funções Auxiliares (`call_agent` para executar os agentes e interagir com LangSmith, `to_markdown` para formatar a saída).
*   **PASSO 7:** Definição dos 4 Agentes Principais (`define_routine_planner_agent`, `define_meal_planner_agent`, `define_activity_coordinator_agent`, `define_progress_coach_agent`). É aqui que a "personalidade" e as instruções de cada agente são moldadas!
*   **PASSO 8:** Lógica Principal de Orquestração, onde os agentes são chamados em sequência, passando informações de um para o outro.

## ⚙️ Como o Sistema Opera: Um Exemplo Prático (How the System Operates: A Practical Example)

Vamos imaginar um cenário típico:

1.  **Início do Dia:** O sistema é iniciado (por exemplo, executando o notebook Colab).
2.  **Inputs do Usuário:**
    *   O sistema pergunta em qual idioma você prefere as saídas (Português ou Espanhol).
        *   *Exemplo: Você escolhe `es-LA`.*
    *   Pede o nome da mãe e do pai (para personalizar algumas saídas).
        *   *Exemplo: Mãe: `Liss`, Pai: `Haroldo`.*
    *   Pergunta a que horas a criança (Zoe) acordou.
        *   *Exemplo: Você digita `8:00 AM`.*
    *   *(Outros inputs como feedback do dia anterior, ingredientes disponíveis, etc., são atualmente simulados no script, mas poderiam ser interativos).*
3.  **Execução dos Agentes em Cadeia:**

    *   **Etapa 1: Agente Planejador de Rotina Adaptativa (`AdaptiveRoutinePlanner`)**
        *   **Entrada (para o agente):** Data atual, nome da criança, idade, nomes dos pais, feedback do dia anterior (simulado), hora que acordou hoje, idioma de saída (es-LA).
        *   **Ação:** O agente processa essas informações e, usando o modelo Gemini, gera uma sugestão de rotina diária adaptada.
        *   **Saída de Exemplo (em es-LA):**
            ```
            > Rutina Diaria para Zoe - Sábado, 17 de Mayo de 2025
            > Tipo de Día: Tipo B (Energía Moderada)...
            > 
            > Hora de Despertar: 8:00 AM ☀️
            > 
            > Horarios: (...)
            > 8:00 - 8:30 AM: Despertar y Tiempo de Conexión 🥰: ...
            > 8:30 - 9:00 AM: Desayuno 🍓🍌: ...
            > ... (restante da rotina detalhada) ...
            > Nota: Este horario es una guía. Ajusta según las necesidades de Zoe.
            ```

    *   **Etapa 2: Agente Chef Nutricional (`NutritionalChefAssistant`)**
        *   **Entrada:** Ingredientes disponíveis (simulados), preferências da família, necessidades da Zoe, nome da Zoe, idioma de saída (es-LA), modo de planejamento ("daily").
        *   **Ação:** O agente gera um plano de refeições para o dia.
        *   **Saída de Exemplo (em es-LA):**
            ```
            > NutriChefAI - Plan de comidas diario para hoy
            > 
            > Desayuno:
            > *   Padres: Avena con plátano y nueces...
            > *   Zoe: Papilla de avena con plátano machacado...
            > ... (restante do plano de refeições) ...
            ```

    *   **Etapa 3: Agente Coordenador de Atividades (`ActivityCoordinator`)**
        *   **Entrada:** Recursos da casa (simulados), clima (simulado), disponibilidade do cuidador (simulada), nome e idade da Zoe, humor (simulado), idioma de saída (es-LA).
        *   **Ação:** O agente sugere atividades de desenvolvimento.
        *   **Saída de Exemplo (em es-LA):**
            ```
            > Sugestões de Atividades para Hoje:
            > 
            > 1.  **Construcción Libre con Bloques (Juego Autónomo):** Deja que Zoe explore...
            >     *Beneficio: Desarrolla la creatividad...*
            > 2.  **Dibujo Creativo (Con o sin Cuidador):** Ofrece a Zoe crayones...
            > ... (restante das atividades sugeridas) ...
            ```
    *   **Etapa 4: Agente Coach de Progresso (`ProgressCoachEvaluator`)** (se ativado para execução diária/semanal)
        *   **Entrada:** Logs semanais (simulados), feedback do cuidador (simulado), metas da família, nome da Zoe, idioma de saída (es-LA).
        *   **Ação:** O agente analisa o progresso e oferece recomendações.
        *   **Saída de Exemplo (em es-LA):**
            ```
            > Relatório Semanal e Recomendações
            > 
            > **Pontos Positivos da Semana:**
            > *   Parabéns! Parece que Zoe se adaptou bem...
            > **Pequenos Desafios e Observações:**
            > *   As noites de terça e quinta foram um pouco mais agitadas...
            > **Recomendações para a Próxima Semana:**
            > 1.  **Rotina Noturna:** Considerem adicionar um banho morno...
            ```
4.  **Resultado Final:** O usuário (você, neste caso) recebe as saídas de cada agente, formatadas para fácil leitura, no idioma selecionado.

## 🌊 Fluxo de Orquestração do Sistema (System Orchestration Flow)

O sistema opera através de uma **orquestração sequencial** dos agentes, onde a saída de um agente pode informar a entrada ou o contexto para os próximos. A lógica principal no notebook (PASSO 8) gerencia este fluxo:

```mermaid
graph LR
    A[Input do Usuário (Tópico/Necessidade Inicial, Idioma)] --> B{PASSO 8: Orquestrador Principal};
    B --> C(Instancia AgenteRutina com dados atuais);
    C --> D{call_agent(AgenteRutina)};
    D --> E[Rotina Diária Gerada];
    B --> F(Instancia AgenteAlimentacion com dados atuais);
    F --> G{call_agent(AgenteAlimentacion)};
    G --> H[Plano de Refeições Gerado];
    B --> I(Instancia AgenteActividades com dados atuais);
    I --> J{call_agent(AgenteActividades)};
    J --> K[Sugestões de Atividades Geradas];
    B --> L(Instancia AgenteCoach com dados semanais);
    L --> M{call_agent(AgenteCoach) - Opcional/Semanal};
    M --> N[Relatório e Recomendações];
    
    E --> O((Output para Usuário));
    H --> O;
    K --> O;
    N --> O;

    subgraph "Observabilidade (LangSmith)"
        D --> LS1[Trace: AgenteRutina];
        G --> LS2[Trace: AgenteAlimentacion];
        J --> LS3[Trace: AgenteActividades];
        M --> LS4[Trace: AgenteCoach];
    end

    style A fill:#D5F5E3,stroke:#2ECC71
    style B fill:#EBF5FB,stroke:#3498DB
    style O fill:#FCF3CF,stroke:#F1C40F
    style LS1 fill:#FDEDEC,stroke:#E74C3C
    style LS2 fill:#FDEDEC,stroke:#E74C3C
    style LS3 fill:#FDEDEC,stroke:#E74C3C
    style LS4 fill:#FDEDEC,stroke:#E74C3C
