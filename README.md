# Notificações Inteligentes — PoC LiteRT-LM + Gemma


[![Android CI](https://github.com/pedrobelota/android-smart-notifications/actions/workflows/android.yml/badge.svg)](https://github.com/pedrobelota/android-smart-notifications/actions/workflows/android.yml)
[![Security](https://github.com/pedrobelota/android-smart-notifications/actions/workflows/security.yml/badge.svg)](https://github.com/pedrobelota/android-smart-notifications/actions/workflows/security.yml)

**IA generativa no dispositivo:** integração de Gemma 4 E2B com LiteRT-LM para transformar rajadas de notificações em resumos em português. O trabalho reúne engenharia de prompt, streaming de tokens, gestão de recursos nativos, preparação de dados para SFT e integração Android — sem depender de uma API de LLM em nuvem durante a inferência.

**Guia para avaliação técnica:** [evidências, autoria e limites](docs/EVIDENCE.md) · [model card](MODEL_CARD.md) · [dataset](dataset_optimized/README.md) · [testes](app/src/test/java/br/edu/devtitans/smartnotifications/ai).

O status de conclusão abaixo refere-se à PoC de bancada relatada; a integração AOSP e a validação de produção permanecem pendentes.
**STATUS: CONCLUÍDO (PoC Validada On-Device)**

Repositório independente de portfólio de Pedro Henrique, derivado da branch
`feat/poc-litert-gemma` do [projeto colaborativo DevTitans](https://github.com/miguelmoraesx/android-smart-notifications),
com histórico e autoria dos colaboradores preservados. A documentação de fechamento
é mantida nesta cópia; ela não transfere a autoria exclusiva do projeto nem atribui
uma nova licença ao código original.

Hands-on Final DevTitans — Turma 9. A PoC captura notificações externas autorizadas pelo Android, agrupa rajadas e gera um resumo local, sem API de inferência em nuvem. A integração AIDL com AOSP/SystemUI é a próxima fase.

## Validação em hardware físico

Resultados de bancada informados pelo responsável pelo projeto, consolidados em 30/10/2026. Esta revisão documental não repetiu os testes ADB nem produziu um benchmark independente.

| Item | Observação de bancada |
| --- | --- |
| Dispositivo | Motorola XT2125-4 / Moto G100, Snapdragon 870 |
| Sistema | Android 17, conforme ambiente informado; registrar build fingerprint em futuras medições |
| Inferência por lote de 3 mensagens | Aproximadamente 2,5–3,2 s; amostra e percentis não registrados |
| Memória | Aproximadamente 2,4 GB informados; PSS/RSS não fornecidos, não confundir com tamanho do arquivo |
| CPU | Até 4 threads nativas |
| Debounce | 5 s de silêncio antes da inferência |

O teste relatado utilizou `adb shell cmd notification post`, com origem `com.android.shell`, simulando contextos como Slack, WhatsApp e alertas DevOps. A captura externa, o agrupamento, o card `Resumo de 3 notificações` e a trava anti-loop foram validados. Isso demonstra independência do mock interno; não constitui teste direto de todos esses aplicativos nem garantia de acesso a qualquer notificação.

A latência de inferência não inclui os cinco segundos de debounce, importação do modelo ou carregamento inicial. Ausência de OOM nos cenários relatados não elimina o risco em outros aparelhos ou cargas.

## Arquitetura implementada

```text
SmartNotificationListenerService (permissão do usuário)
  → NotificationViewer (lote + debounce de 5 s)
  → SummaryGenerator → PromptBuilder
  → LLMManager → LiteRT-LM 0.17.0 → Gemma 4 E2B
  → card Android no canal smart_summary_channel
```

`SmartNotificationsApplication` mantém uma instância compartilhada de `LLMManager`, `LocalModelStore`, `SummaryGenerator` e `NotificationViewer` durante a vida do processo. Isso permite reutilizar o engine carregado entre lotes; não garante permanência dos pesos em RAM nem sobrevivência à destruição do processo pelo Android. O usuário ainda precisa selecionar e inicializar o modelo.

O listener descarta notificações do próprio pacote no canal `smart_summary_channel`, evitando recursão. A tela manual permanece disponível para diagnóstico. A captura depende das permissões e das restrições do sistema operacional.

## Prompt e limites de inferência

**Dataset no Hugging Face:** [phbg/smart-notifications-synthetic](https://huggingface.co/datasets/phbg/smart-notifications-synthetic),
com 3.707 exemplos sintéticos, splits, auditoria e proveniência. Sua publicação não
significa que o Gemma utilizado tenha sido treinado nesses dados.
Veja também a [coleção de datasets e modelos utilizados](https://huggingface.co/collections/phbg/devtitans-and-pibic-ai-engineering-6ae553217b5be2d991b7e904),
com atribuição dos checkpoints de terceiros.

`PromptBuilder` normaliza linhas, remove duplicatas e mantém até 1.600 caracteres recentes do conteúdo. O prompt completo inclui também estas instruções:

```text
Resuma as notificações em português do Brasil, em um parágrafo de no máximo 25 palavras.
Preserve nomes, datas, horários, prazos e ações atuais. Ignore repetições, ruído e fatos corrigidos.
Não invente informações. Responda somente com o resumo, sem Markdown.
<mensagens>
{texto_normalizado}
</mensagens>
```

| Configuração | Valor e finalidade |
| --- | --- |
| `temperature` | 0.1: reduz diversidade; não garante determinismo ou factualidade |
| `topK` / `topP` | 20 / 0.8: restringem a distribuição de amostragem |
| `noRepeatNgramSize` | 4: reduz repetições |
| `maxOutputToken` | 48: limita geração; tokens não equivalem a palavras |
| Contexto | 768 tokens, para conter o KV cache |
| CPU | `availableProcessors().coerceIn(1, 4)` |

`sanitizeSummary()` remove cabeçalhos como “Resumo:” e formatação indesejada. O teto de 25 palavras é uma instrução, não uma garantia de contagem; alucinação e prompt injection continuam possíveis. Limitar contexto reduz o KV cache, cujo crescimento não deve ser descrito como exponencial. Quatro threads reduzem concorrência com a UI, mas não reservam fisicamente os demais núcleos.

O `dataset_optimized/` fornece pares `input`/`output`, alvos de até 25 palavras e exemplos de correções de estado que orientam o formato da tarefa. É procedural, com pouca diversidade em algumas categorias; não comprova qualidade em produção nem que o checkpoint distribuído tenha sido treinado nesses dados. Consulte seu [README](dataset_optimized/README.md).

## Executar e verificar

Para experimentar sem compilar, abra uma execução bem-sucedida do [Android CI](https://github.com/pedrobelota/android-smart-notifications/actions/workflows/android.yml)
e baixe o artefato `smart-notifications-demo-and-tests` (retido por 14 dias; o GitHub pode exigir login).
Ele inclui APK de debug e relatórios de testes. Os pesos precisam ser obtidos separadamente;
é uma demonstração de pesquisa, não uma versão de produção.

Requer JDK 17, Android SDK 37 e Android Studio compatível com AGP 9.1.1. O projeto usa Kotlin 2.4.20 e Gradle 9.3.1. Para a bancada, prefira dispositivo ARM64 com memória e armazenamento suficientes.

```powershell
.\gradlew.bat testDebugUnitTest assembleDebug
```

Em Linux/macOS, use `./gradlew testDebugUnitTest assembleDebug`. APK: `app/build/outputs/apk/debug/app-debug.apk`.

1. Instale o APK e conceda acesso às notificações nas configurações do Android e permissão de postagem quando solicitada.
2. Baixe o artefato compatível descrito no [MODEL_CARD.md](MODEL_CARD.md).
3. Selecione o `.litertlm` no app e aguarde “Modelo pronto”. O arquivo é copiado para o armazenamento privado.
4. Envie notificações de teste sem dados pessoais, aguarde o debounce e confira o resumo e a ausência de recursão.

O modelo não está incluído no APK. Inferência offline não equivale a privacidade absoluta: esta revisão removeu o conteúdo das mensagens, os resumos e detalhes de exceções dos logs de geração. Isso não constitui garantia de privacidade absoluta; use dados sintéticos e revise backup, permissões e exposição do receiver de teste antes de produção. Android pode suspender ou encerrar o processo sob pressão de memória.

## Próxima fase

**Experimento de fine-tuning preparado, ainda não executado:**
[abrir piloto QLoRA no Colab](https://colab.research.google.com/github/pedrobelota/android-smart-notifications/blob/feat/poc-litert-gemma/notebooks/notification_qlora_pilot.ipynb).
O notebook compara Gemma 3 1B IT antes/depois de um piloto LoRA de 64 passos,
com dataset fixado por revisão, alvos mascarados e exportação de adaptador e relatório.
Requer acesso ao modelo e uma GPU gratuita compatível disponível; não contrata
recursos nem publica modelos automaticamente. As células passaram por análise
sintática e a preparação dos 3.707 exemplos foi verificada com o tokenizer real;
execução de treinamento em GPU e compatibilidade completa das dependências no Colab
ainda precisam ser verificadas. O modelo Android Gemma 4 E2B permanece separado.
Consulte o [protocolo](docs/finetuning-experiment.md). Não há resultado de treinamento
ou ganho de qualidade atribuído a esse notebook nesta etapa.

Criar um contrato AIDL assíncrono entre SystemUI e um serviço de inferência em **processo separado**, com autenticação/permissões, fila limitada, cancelamento, timeouts e recuperação após morte do Binder. Não carregar o modelo dentro de SystemUI ou system_server. A integração Soong/AOSP, a política de ciclo de vida e os testes sob pressão de memória ainda não estão concluídos.

Veja as [notas de entrega](RELEASE_NOTES.md) e o [relatório de bancada](STATUS_REPORT_POC.md).
