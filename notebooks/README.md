# Experimento de treinamento

`notification_qlora_pilot.ipynb` é um experimento separado da PoC Android validada em bancada. A execução de 64 passos foi concluída em uma Tesla T4 e gerou um adaptador LoRA. Manter o código no GitHub permite revisar e reproduzir o método; a execução concluída não comprova, sozinha, que o modelo ficou melhor.

O arquivo versionado permanece sem saídas de execução e sem credenciais. Os resultados revisados estão em [`docs/finetuning-results.md`](../docs/finetuning-results.md), e o adaptador está no [Hugging Face](https://huggingface.co/phbg/gemma-3-1b-smart-notifications-qlora-pilot). As pastas de execução e os pesos gerados continuam ignorados pelo Git.

## Correção de compatibilidade

Transformers 5.22 retorna um dicionário por padrão em `apply_chat_template()`. A preparação dos exemplos pede explicitamente `return_dict=False` para obter listas de IDs; a geração pede `return_dict=True` para alimentar o modelo. O erro `Unexpected template boundary` identificado no primeiro ensaio era causado por esse contrato incorreto.

Cada tentativa de preparação recebe uma pasta de saída nova para preservar tentativas anteriores. A geração informa progresso por exemplo. O teste opcional `python tools/check_training_tokenization.py` verifica os limites entre prompt/resposta e o mascaramento dos alvos com o tokenizer real, sem baixar os pesos nem treinar. Requer Transformers e acesso autorizado ao tokenizer do Gemma.

Na revisão de 30/10/2026, esse teste passou nos 3.707 exemplos: 2.965 de treino,
371 de validação e 371 de teste, todos dentro de 768 tokens após aplicar o template.
Foi uma verificação de preparação/tokenização, sem inferência ou ajuste de pesos
e sem avaliação da qualidade dos resumos no conjunto de teste.

O pacote exportado registrou 512 exemplos de treino, 16 de validação, 64 passos,
104 tensores treináveis alterados, 286,34 segundos de execução e pico de memória
GPU de 2.948.267.008 bytes. Modelo-base e adaptador produziram 16/16 respostas não
vazias e com até 25 palavras, mas a revisão qualitativa encontrou erros factuais e
temporais. O split de teste não foi usado.
