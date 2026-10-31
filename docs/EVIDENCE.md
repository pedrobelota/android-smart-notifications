# Evidências técnicas e escopo de autoria

Este portfólio apresenta uma aplicação de IA generativa on-device: um LLM produz texto novo condicionado às notificações, usando pesos públicos e inferência nativa local. Não é um chatbot de respostas fixas nem uma chamada a uma API de LLM em nuvem.

## O que um avaliador pode inspecionar

| Competência | Evidência no repositório | Limite da afirmação |
| --- | --- | --- |
| Integração e execução de LLM | `LLMManager.kt`: Engine, Conversation, Flow, Mutex, fechamento de recursos | Integra checkpoint existente; não treina um modelo fundamental |
| Engenharia de prompt | `PromptBuilder.kt` e seus testes: normalização, deduplicação, recência, 1.600 caracteres | Prompt não garante factualidade nem resistência a injeção |
| Otimização edge | CPU até 4 threads, contexto 768, saída 48 tokens, emissões em blocos de 32 caracteres | Configuração verificável; ganhos precisam de benchmark controlado |
| Engenharia de dados | `dataset_optimized/`, relatório e `tools/verify_dataset.py` | 3.707 exemplos procedurais; não prova fine-tuning ou generalização |
| Integração Android | Listener real, debounce 5 s e canal de resumo com anti-loop | Ignora android/SystemUI; depende das permissões do SO |
| Testabilidade | Testes JVM de prompt, sanitização e caso de uso; CI com build do APK | Não substitui execução do runtime nativo no aparelho |
| Validação física | Relato de bancada no README e STATUS_REPORT_POC.md | Sem logs brutos, vídeo, hashes do modelo ou benchmark independente publicados |

## Autoria e assistência de IA

Validação independente de software em 30/10/2026: o [Android CI](https://github.com/pedrobelota/android-smart-notifications/actions/runs/41158328323)
executou `testDebugUnitTest assembleDebug` com sucesso em JDK 17/Linux. A validação
do dataset confirmou 2.965 exemplos de treino, 371 de validação e 371 de teste,
sem entradas duplicadas entre splits e com saídas de até 25 palavras. O ZIP contém
os mesmos cinco arquivos publicados, equivalentes após normalizar finais de linha.
Gitleaks não encontrou segredos no histórico examinado. Não havia dispositivo ADB
autorizado conectado nesta revisão. Esses resultados não comprovam factualidade
dos resumos, generalização ou desempenho físico do modelo.

Projeto colaborativo DevTitans, com histórico original preservado. O relatório atribui a frente LLM a Pedro Henrique e a frente AOSP a outro colaborador. O histórico permite inspecionar as contribuições; não se reivindica autoria exclusiva do sistema.

Assistentes de IA foram usados na revisão técnica, documentação e manutenção deste portfólio. Essa assistência não substitui a responsabilidade do autor por explicar o código e os resultados. Não há evidência publicada de um checkpoint próprio treinado com o dataset; a expressão correta é integração de LLM e preparação de dados para eventual SFT.

## Como fortalecer a evidência de bancada

Registrar commit, SHA-256/revisão do modelo, build fingerprint, condições de execução e número de repetições. Usar somente notificações sintéticas, capturar tempo de carregamento separado de inferência e debounce, reportar mediana/p95 e PSS/RSS, incluindo falhas. Uma gravação curta pode mostrar captura externa → lote → inferência → card final, sem dados pessoais.

Avaliar retenção de entidades, correções de horário, limite de palavras e informações inventadas em exemplos não usados para ajustar o prompt. Ainda faltam testes automatizados de debounce/concorrência, morte do processo e pressão de memória. O receiver de mock permanece exportado para bancada e deve ser restrito antes de distribuição de produção. O suporte declarado desde API 24 precisa ser revisto frente ao uso de canais de notificação (API 26).

## Complementaridade do portfólio

[Coach Emotion Analysis](https://github.com/pedrobelota/coach-emotion-analysis) demonstra pesquisa, integração de modelos de áudio, avaliação e entrega de API. Este projeto demonstra geração com LLM, engenharia Android e restrições de inferência edge. Cada um sustenta competências diferentes; nenhum resultado de um valida o outro.
