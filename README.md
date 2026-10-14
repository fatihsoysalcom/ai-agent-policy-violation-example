# AI Agent Policy Violation Example

This example demonstrates how an AI agent, even with successful tool calls, can violate company policies. It simulates an agent retrieving order details and sending a customer response via email. The agent's decision to include sensitive Personally Identifiable Information (PII) in the email, despite the email sending tool working correctly, triggers a policy violation check. A second scenario shows a policy-aware agent avoiding the violation.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal using `python main.py`.

## Original Article

This example accompanies the Turkish article: [Yapay Zeka Ajanları Neden Şirket Politikalarını İhlal Eder? Tüm Araç Çağrıları Başarılı Olsa Bile](https://fatihsoysal.com/blog/yapay-zeka-ajanlari-neden-sirket-politikalarini-ihlal-eder-tum-arac-cagrilari-basarili-olsa-bile/).

## License

MIT — see [LICENSE](LICENSE).
