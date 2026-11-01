# Resultados do piloto QLoRA

## Conclusão correta

O treinamento piloto foi concluído e produziu um adaptador LoRA próprio sobre o
checkpoint público `google/gemma-3-1b-it`. Isso demonstra preparação de dados,
fine-tuning eficiente em parâmetros, rastreabilidade e análise de resultados. Não
significa treinamento de um modelo fundamental nem comprova melhoria geral sobre o
modelo-base.

O adaptador e os arquivos de avaliação estão publicados em
[`phbg/gemma-3-1b-smart-notifications-qlora-pilot`](https://huggingface.co/phbg/gemma-3-1b-smart-notifications-qlora-pilot).

## Execução registrada

| Item | Resultado |
| --- | --- |
| Modelo-base | Gemma 3 1B IT, revisão `dcc83ea841ab6100d6b47a070329e1ba4cf78752` |
| Dataset | `phbg/smart-notifications-synthetic`, revisão `7cb29736e49ed7dd4de6b31bf5d3ff033fa9e316` |
| Método | QLoRA/NF4, LoRA `r=8`, `alpha=16`, módulos `q_proj` e `v_proj` |
| Amostras | 512 treino + 16 validação; teste não utilizado |
| Execução | 64 passos, uma época, 286,34 s em Tesla T4 |
| Memória GPU de pico | 2.948.267.008 bytes |
| Tensores treináveis alterados | 104 |
| Loss de treino agregada | 1,5349 |
| Loss de validação | 1,2532 no passo 32; 1,0369 no passo 64 |

## O que a avaliação mostrou

Modelo-base e adaptador geraram 16/16 saídas não vazias e com até 25 palavras. Essa
checagem confirma o formato, não a factualidade. A inspeção qualitativa encontrou:

- respostas adaptadas mais curtas e próximas do estilo esperado em vários casos;
- uma data inexistente adicionada a um código de autenticação;
- perda de entidades em um convite para consulta;
- mistura entre uma corrida cancelada e o novo motorista em dois exemplos;
- erros também presentes no modelo-base, inclusive informação inventada e estado final incorreto.

A amostra é pequena, não houve revisão cega e não foi calculada significância. Por
isso, o resultado deve ser descrito como **fine-tuning executado e auditável, com
qualidade ainda não validada**.

## Relação com o aplicativo Android

O piloto usa Gemma 3 1B IT porque cabe no ambiente gratuito de treinamento. A PoC
Android usa um artefato Gemma 4 E2B no LiteRT-LM. O adaptador publicado não é usado
diretamente pelo aplicativo; converter, compatibilizar e medir uma variante adequada
é uma etapa futura.

## Próximos passos

1. Congelar uma rubrica para entidades, valores, temporalidade, estado final e alucinação.
2. Fazer revisão humana cega no split de teste, sem reutilizá-lo para ajustar o modelo.
3. Comparar modelo-base, adaptador e referência por categoria de notificação.
4. Repetir o treinamento com outras sementes e reportar variação.
5. Só depois avaliar conversão para um runtime on-device compatível.
