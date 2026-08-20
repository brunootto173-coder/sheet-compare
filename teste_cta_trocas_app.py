from app.services.cta_trocas import executar_comparacao


resultado = executar_comparacao(
    "BASE CTA.xlsx",
"26-06-2026 troca normal.xlsx",
)


print("=" * 60)
print("RESULTADO CTA x TROCAS")
print("=" * 60)

for chave, valor in resultado["resumo"].items():
    print(f"{chave}: {valor}")