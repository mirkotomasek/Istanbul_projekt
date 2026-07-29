# Cesta do Istanbulu

Statický cestovní deník publikovaný přes GitHub Pages a spravovaný
přes Pages CMS.

## Přidání nového dne z mobilu

1. Nahraj hlasovou zprávu do připraveného vlákna v ChatGPT.
2. Zkopíruj číslo dne, datum, nadpis, odkud, kam a text.
3. Otevři Pages CMS a přihlas se přes GitHub.
4. Otevři sekci **Denní zápisky**.
5. Klepni na **New**, vyplň pole a nahraj fotografie.
6. Klepni na **Save**.

GitHub Pages následně web automaticky znovu sestaví.

Nadpis má vystihnout příběh dne a nemá obsahovat trasu. Výchozí a
cílové místo patří pouze do polí **Odkud** a **Kam**, ideálně s vlajkou
země (například `🇷🇸 Mol` → `🇷🇸 Zrenjanin`).

## Struktura

- `_days/den-N.md` – jednotlivé zápisky;
- `media/` – fotografie;
- `index.html` – vzhled a Jekyll šablona;
- `.pages.yml` – konfigurace Pages CMS;
- `_config.yml` – konfigurace Jekyllu;
- `CHATGPT-PROMPT.md` – pokyn pro hlasové zápisky.

Jednotlivé dny jsou ve výchozím stavu sbalené. Kliknutím na hlavičku
se zápisek rozbalí.
