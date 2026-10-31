# Experimento de treinamento

`notification_qlora_pilot.ipynb` é um experimento em andamento, separado da PoC Android validada em bancada. Manter o código no GitHub permite revisar e reproduzir o método; a presença do notebook não comprova que o treinamento terminou ou melhorou o modelo.

O arquivo versionado deve permanecer sem saídas de execução e sem credenciais. Registre resultados reais em um relatório revisado; publique pesos/adaptadores no Hugging Face somente com proveniência e avaliação. As pastas de execução e os pesos gerados são ignorados pelo Git.

## Correção de compatibilidade

Transformers 5.22 retorna um dicionário por padrão em `apply_chat_template()`. A preparação dos exemplos pede explicitamente `return_dict=False` para obter listas de IDs; a geração pede `return_dict=True` para alimentar o modelo. O erro `Unexpected template boundary` identificado no primeiro ensaio era causado por esse contrato incorreto.

Cada tentativa de preparação recebe uma pasta de saída nova para preservar tentativas anteriores. A geração informa progresso por exemplo. O teste opcional `python tools/check_training_tokenization.py` verifica os limites entre prompt/resposta e o mascaramento dos alvos com o tokenizer real, sem baixar os pesos nem treinar. Requer Transformers e acesso autorizado ao tokenizer do Gemma.

Na revisão de 30/10/2026, esse teste passou nos 3.707 exemplos: 2.965 de treino,
371 de validação e 371 de teste, todos dentro de 768 tokens após aplicar o template.
Foi uma verificação de preparação/tokenização, sem inferência ou ajuste de pesos
e sem avaliação da qualidade dos resumos no conjunto de teste.

Se o Colab já estava aberto, ele pode manter o código antigo na sessão: atualizar o GitHub não altera automaticamente suas células. Salve resultados importantes antes de trocar de versão. Se apenas a preparação falhou, ainda não há evidência de treinamento concluído.
