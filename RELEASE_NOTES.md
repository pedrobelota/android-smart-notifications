# Notas de entrega — PoC validada on-device

Status: CONCLUÍDO (PoC Validada On-Device), conforme bancada relatada pelo responsável. Escopo: branch `feat/poc-litert-gemma`.

- README atualizado para refletir captura externa, debounce de cinco segundos, engine compartilhado e proteção anti-loop já implementados.
- Documentadas configurações de prompt, amostragem, contexto e CPU verificadas no código.
- Adicionada model card com proveniência, download, requisitos de conversão e limites de reprodução.
- Métricas de dispositivo identificadas como resultados relatados, sem alegar nova medição nesta revisão.
- Explicitados riscos remanescentes: pressão de memória, factualidade e permissões Android; os logs com conteúdo identificados inicialmente foram removidos na revisão de portfólio.

Próxima fase: contrato AIDL assíncrono e serviço de inferência em processo próprio, integrado ao SystemUI por Binder. Não executar a LLM dentro de SystemUI ou system_server. Integração AOSP, proteção de acesso e testes de resiliência ficam para essa etapa.
