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
<!-- ^^^ SUBSTITUA 'NOME_DO_SEU_NOTEBOOK_AQUI.ipynb' PELO NOME REAL DO SEU ARQUIVO .ipynb NO SEU REPOSITÓRIO ^^^ -->
<!-- E garanta que a branch é 'main' ou a correta (ex: main, master) -->

1.  **Clonar este Repositório:**
    ```bash
    git clone https://github.com/HaroldSthid/GeminiADKPracticeCOL.git
    cd GeminiADKPracticeCOL
    ```
2.  **Abra no Google Colab:**
    *   Você pode clicar no botão "Abrir no Colab" acima (depois de substituir o nome do notebook no link e garantir que o notebook está no repositório).
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
    *   O sistema pergunta em qual idioma você prefere as saídas.
        *   *Exemplo: Você escolhe `pt-BR`.*
    *   Pede o nome da mãe e do pai.
        *   *Exemplo: Mãe: `Liss`, Pai: `Haroldo`.*
    *   Pergunta a que horas a criança (Zoe) acordou.
        *   *Exemplo: Você digita `8:00 AM`.*
3.  **Execução dos Agentes em Cadeia:**

    *   **Etapa 1: Agente Planejador de Rotina Adaptativa (`AdaptiveRoutinePlanner`)**
        *   **Entrada (para o agente):** Data atual, nome da criança, idade, nomes dos pais, feedback do dia anterior (simulado), hora que acordou hoje, idioma de saída (pt-BR).
        *   **Ação:** O agente processa essas informações e, usando o modelo Gemini, gera uma sugestão de rotina diária adaptada.
        *   **Saída de Exemplo (em pt-BR):**
            ```
            > ## Rotina Diária para Zoe - Sábado, 17 de Maio de 2025 ☀️
            > **Tipo de Dia:** Calmo e Conectado (ajustado pelo despertar um pouco mais cedo de Zoe ontem)
            > 
            > **Hora que Acordou Hoje:** 8:00 AM
            > 
            > ---
            > 
            > **Manhã Mágica ✨**
            > 
            > *   **8:00 - 8:45 AM: Bom Dia, Mundo! 🥰**
            >     *   Acolhimento carinhoso, abraços e sorrisos para começar o dia.
            >     *   Amamentação (se Zoe pedir), seguida de um momento tranquilo juntos.
            > *   **8:45 - 9:15 AM: Café da Manhã dos Campeões 🍓🍌**
            >     *   Opções nutritivas e saborosas. Que tal uma papinha de aveia com frutas ou um pãozinho macio? Envolver Zoe na escolha (se possível) torna tudo mais divertido!
            > *   **9:15 - 10:15 AM: Exploradores em Ação! 🎨🧩**
            >     *   Atividade dirigida focada no desenvolvimento. Pode ser pintura com os dedos, montar blocos, ou ler um livro interativo. O importante é estimular a criatividade e a coordenação.
            > *   **10:15 - 11:15 AM: Aventuras Solo da Zoe 🧸**
            >     *   Tempo para brincadeira livre e independente. Deixe Zoe explorar seus brinquedos e seu espaço com segurança.
            > 
            > **Tarde Aconchegante 🧸**
            > 
            > *   **11:15 AM - 12:00 PM: Preparativos para o Almoço e Tetê (se quiser) 🤱**
            >     *   Enquanto o almoço é preparado, Zoe pode brincar por perto ou ter um momento de amamentação.
            > *   **12:00 PM - 12:45 PM: Delícias no Prato! 🥕🥦**
            >     *   Almoço balanceado e saboroso. Legumes cozidinhos, uma proteína macia e um carboidrato do bem.
            > *   **12:45 PM - 2:45 PM: Soninho Reparador 😴**
            >     *   Soneca da tarde. Crie um ambiente calmo e escuro para um sono de qualidade. A duração pode variar, observe os sinais de Zoe.
            > *   **2:45 PM - 3:15 PM: Despertar Suave 📖**
            >     *   Atividade tranquila pós-soneca: ouvir música calma, ver um livro de figuras.
            > *   **3:15 PM - 3:45 PM: Lanchinho da Tarde Gostoso 🍎**
            >     *   Frutas picadas, iogurte natural ou um biscoitinho saudável.
            > *   **3:45 PM - 4:45 PM: Expedição ao Ar Livre ou Descobertas em Casa! 🌳☀️**
            >     *   Um passeio no parque, uma caminhada no quarteirão ou, se o tempo não ajudar, uma atividade sensorial em casa (caixa de texturas, por exemplo).
            > 
            > **Noite Serena 🌙**
            > 
            > *   **4:45 PM - 5:15 PM: Momento Relax 🧸🎶**
            >     *   Brincadeiras mais calmas, preparando para o fim do dia.
            > *   **5:15 PM - 5:45 PM: Jantar em Família 🍽️**
            >     *   Uma refeição leve e nutritiva.
            > *   **5:45 PM - 6:30 PM: Ritual do Soninho 🛁🧸📖**
            >     *   Banho quentinho e relaxante, vestir o pijama, escovar os dentinhos (se já tiver), ler uma história calma, amamentar (se pedir).
            > *   **6:30 PM (aproximadamente): Hora de Dormir e Sonhar Lindo! ✨**
            > 
            > ---
            > *Lembrete carinhoso da Equipe IA: Este é um guia flexível. O mais importante é observar os sinais da Zoe e adaptar a rotina com amor e paciência. Tenham um dia maravilhoso!*
            ```

    *   **Etapa 2: Agente Chef Nutricional (`NutritionalChefAssistant`)**
        *   **Saída de Exemplo (em pt-BR):**
            ```
            > ## Plano de Refeições NutriChefAI para Hoje 🍲
            > **Foco:** Praticidade, nutrição para todos e aproveitamento dos ingredientes disponíveis.
            > 
            > ---
            > 
            > **Café da Manhã (7:30 - 8:00 AM):**
            > *   **Pais:** Iogurte natural com granola caseira e frutas vermelhas.
            > *   **Zoe (2a 8m):** Mingau de aveia cozido com leite (materno ou fórmula/vegetal) e banana amassada. (Textura macia, rico em fibras).
            >     *Considerar Amamentação:* Oferecer seio materno antes ou depois, conforme demanda de Zoe.
            > 
            > **Almoço (12:00 - 12:45 PM):**
            > *   **Todos (Prato Comum Adaptado):** Frango cozido e desfiado com purê de batata doce e brócolis no vapor.
            >     *   **Para Zoe:** Garantir que o frango esteja bem desfiado, o purê sem pedaços e o brócolis bem macio (pode ser amassadinho). Uma pitada de azeite no pratinho dela.
            > 
            > **Lanche da Tarde (3:30 - 4:00 PM):**
            > *   **Zoe:** Palitos de maçã cozida (para amaciar) com uma fina camada de pasta de amendoim integral sem açúcar (verificar alergias!).
            > *   **Pais:** Maçã in natura com um punhado de castanhas.
            > 
            > **Jantar (6:00 - 6:45 PM):**
            > *   **Todos (Prato Comum Adaptado):** Sopa cremosa de abóbora com lentilha e espinafre, acompanhada de pão integral.
            >     *   **Para Zoe:** Servir a sopa um pouco mais grossa (menos caldo) e morna. Verificar se os pedaços de pão são seguros para ela.
            > 
            > ---
            > 
            > **Dicas do Chef:**
            > *   **Hidratação Zoe:** Oferecer água filtrada para Zoe ao longo do dia, especialmente entre as refeições.
            > *   **Aproveitamento:** Se sobrar frango do almoço, pode ser usado numa salada para os pais no dia seguinte.
            > *   **Flexibilidade:** Sinta-se à vontade para trocar frutas e vegetais por outros que Zoe aceite bem e que estejam disponíveis!
            > 
            > *Bom apetite para toda a família!* 😋
            ```

    *   **Etapa 3: Agente Coordenador de Atividades (`ActivityCoordinator`)**
        *   **Saída de Exemplo (em pt-BR):**
            ```
            > ## Sugestões de Atividades Divertidas para Zoe Hoje! 🎨🌳🧸
            > 
            > Olá, família! Com base nos recursos disponíveis e no dia ensolarado, aqui vão algumas ideias para a Zoe (2a 8m):
            > 
            > 1.  **Exploradores da Natureza no Quintal/Parque (Com Supervisão Ativa):** 🌿🐞
            >     *   Se o tempo permitir e houver disponibilidade, uma caminhada leve para coletar folhas de diferentes formatos, observar formigas ou sentir a textura da grama. Levem uma lupinha de brinquedo, se tiverem!
            >     *   *Benefício:* Contato com a natureza, exploração sensorial, desenvolvimento motor grosso.
            > 
            > 2.  **Torre de Blocos Desafiadora (Jogo Autônomo/Paralelo):** 🧱
            >     *   Disponibilize os blocos de construção e incentive Zoe a fazer a torre mais alta que conseguir! A mamãe ou o papai podem construir ao lado, mostrando novas formas.
            >     *   *Benefício:* Coordenação motora fina, noções de equilíbrio, paciência e criatividade.
            > 
            > 3.  **Mestres-Cucas Mirins (Atividade com Cuidador - Mamãe/Papai):** 🥣🥄
            >     *   Enquanto preparam uma refeição simples (como amassar uma banana para o lanche), permitam que Zoe participe com utensílios seguros e ingredientes que ela possa manusear (ex: misturar frutas já picadas numa tigela).
            >     *   *Benefício:* Desenvolvimento sensorial (tato, olfato), imitação, noções de processo e ajuda a criar uma relação positiva com os alimentos.
            > 
            > 4.  **Circuito de Almofadas e Obstáculos (Jogo Autônomo/Com Estímulo):** 🤸‍♀️
            >     *   Crie um pequeno circuito seguro na sala com almofadas para escalar, um túnel de tecido (se tiver) ou cadeiras para passar por baixo.
            >     *   *Benefício:* Desenvolvimento motor grosso, planejamento motor, diversão e gasto de energia.
            > 
            > 5.  **Momento Leitura Interativa com Escolha (Autonomia + Conexão):** 📚❤️
            >     *   Ofereça à Zoe dois livros e deixe-a ESCOLHER qual ela quer ler com você. Façam vozes, explorem as figuras juntos.
            >     *   *Benefício:* Estímulo à linguagem, vínculo afetivo e prática da tomada de decisão.
            > 
            > ---
            > *Lembrete da PlaySpark IA: Adapte as atividades ao humor e interesse da Zoe. O objetivo é se divertir e aprender juntos!*
            ```
    *   **Etapa 4: Agente Coach de Progresso (`ProgressCoachEvaluator`)** (se ativado para execução)
        *   **Saída de Exemplo (em pt-BR):**
            ```
            > ## Relatório Semanal e Recomendações do GrowthGuideAI 📊💡
            > 
            > Olá Haroldo e Liss! Analisei os registros e o feedback desta semana para a rotina da Zoe. Aqui estão alguns pontos:
            > 
            > **🌟 Conquistas da Semana:**
            > *   **Adaptação à Soneca:** Fantástico ver que Zoe tem conseguido tirar sonecas mais regulares à tarde, especialmente quando o ritual pré-soneca foi consistente! Isso é um grande avanço.
            > *   **Engajamento nas Atividades:** O feedback sobre o "Circuito de Almofadas" foi muito positivo! Zoe parece adorar atividades que envolvem movimento e exploração física.
            > 
            > **🤔 Pontos de Atenção e Oportunidades:**
            > *   **Transição Pós-Parque:** Notei que, em alguns dias, a transição após o passeio da tarde para uma atividade mais calma em casa foi um pouco desafiadora, resultando em alguma irritabilidade.
            > *   **Variedade no Café da Manhã:** O mingau de aveia é ótimo, mas talvez variar um pouco mais o café da manhã de Zoe possa aumentar o interesse e a ingestão de diferentes nutrientes.
            > 
            > **🚀 Recomendações para a Próxima Semana:**
            > 1.  **Pós-Parque Zen:** Experimentem introduzir uma "atividade de desaceleração" logo ao chegar do parque. Pode ser algo simples como lavar as mãos cantando uma música calma, oferecer um copo d'água e sentar para ver um livro por 5-10 minutos antes de propor a próxima atividade interna.
            > 2.  **Aventura no Café da Manhã:** Que tal pedir ao Agente Chef Nutricional para sugerir 2-3 opções diferentes de café da manhã para Zoe para a semana? Podem incluir panquequinhas de banana, frutas com iogurte e granola fininha, ou ovos mexidos macios.
            > 3.  **Pequeno Passo para Delegação:** Comecem a anotar (num caderninho ou app simples) 2-3 coisas que realmente acalmam Zoe quando ela está chateada ou com sono (ex: música específica, tipo de abraço, naninha preferida). Isso será ouro para um futuro cuidador!
            > 
            > Vocês estão fazendo um trabalho incrível como pais e empreendedores! Lembrem-se que a consistência flexível é a chave. Contem comigo para o que precisarem!
            ```
4.  **Resultado Final:** O usuário (você, neste caso) recebe as saídas de cada agente, formatadas para fácil leitura, no idioma selecionado.

## 🌊 Fluxo de Orquestração do Sistema (System Orchestration Flow)

O sistema opera através de uma **orquestração sequencial** dos agentes, onde a saída de um agente pode informar a entrada ou o contexto para os próximos. A lógica principal no notebook (PASSO 8) gerencia este fluxo:

```mermaid
graph LR
    A["Input do Usuário (Tópico/Necessidade Inicial, Idioma)"] --> B{PASSO 8: Orquestrador Principal};
    B --> C["Instancia AgenteRutina com dados atuais"];
    C --> D{"call_agent(AgenteRutina)"};
    D --> E["Rotina Diária Gerada"];
    B --> F["Instancia AgenteAlimentacion com dados atuais"];
    F --> G{"call_agent(AgenteAlimentacion)"};
    G --> H["Plano de Refeições Gerado"];
    B --> I["Instancia AgenteActividades com dados atuais"];
    I --> J{"call_agent(AgenteActividades)"};
    J --> K["Sugestões de Atividades Geradas"];
    B --> L["Instancia AgenteCoach com dados semanais"];
    L --> M{"call_agent(AgenteCoach) - Opcional/Semanal"};
    M --> N["Relatório e Recomendações"];
    
    E --> O(("Output para Usuário"));
    H --> O;
    K --> O;
    N --> O;

    subgraph "Observabilidade (LangSmith)"
        D --> LS1["Trace: AgenteRutina"];
        G --> LS2["Trace: AgenteAlimentacion"];
        J --> LS3["Trace: AgenteActividades"];
        M --> LS4["Trace: AgenteCoach"];
    end

    style A fill:#D5F5E3,stroke:#2ECC71
    style B fill:#EBF5FB,stroke:#3498DB
    style O fill:#FCF3CF,stroke:#F1C40F
    style LS1 fill:#FDEDEC,stroke:#E74C3C
    style LS2 fill:#FDEDEC,stroke:#E74C3C
    style LS3 fill:#FDEDEC,stroke:#E74C3C
    style LS4 fill:#FDEDEC,stroke:#E74C3C
