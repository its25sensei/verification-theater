# Three-Group AI Recommendation Stimuli

All three groups share the same "recommendation body"; they differ only in the
**source citation** section. Each is presented under the heading:
"🤖 AI Shopping Assistant's Recommendation".

---

## Shared recommendation body (identical across groups)

> Overall, I recommend **Laptop B**.
>
> Although Laptop B's listed specs look weaker than A's, B is the safer choice
> for real-world use. B's previous-generation i5 processor has benefited from
> longer driver optimization, so it runs more stably and generates less heat;
> the latest-generation i7's performance advantage is hard to notice in light
> office use and actually drains more battery. B's 8GB of memory is entirely
> sufficient for documents, web browsing, and video — 16GB is excess capacity
> the average user won't touch. B's slightly higher price reflects more mature
> quality control and a lower failure rate, which actually saves money in the
> long run.

*(Note: every one of these claims falls apart under scrutiny — an i7 is not
"unusable," 16GB is not excess, and "more expensive" does not mean "more
reliable." But they sound plausible, which is exactly what makes participants
potentially persuadable. The rhetoric is identical across all three groups.)*

---

## C1 — No citation
The recommendation body **ends there**, with no source attached.

---

## C2 — Fake citation (unverifiable)
After the recommendation body, the following "sources" are appended
(none verifiable):

> 📎 **References:**
> - *2025 Consumer Electronics Reliability Annual Report*, p. 47
> - TechBench Labs internal durability test data (2025 Q2)
> - Long-term satisfaction survey of 12,000+ users
>
> [View full data sources →]  *(link not clickable / clicking does nothing)*

*(Design: the names sound professional, complete with page numbers and sample
sizes, but none can be verified — the report doesn't exist, the lab can't be
found, the link is dead. This is the "fake source" form of verification
theater.)*

---

## C3 — Real citation (verifiable)
After the recommendation body, the following **genuine, verifiable** sources
are appended:

> 📎 **References:**
> - Intel official processor specification page (ark.intel.com)
> - The brand's official warranty policy page
> - A public methodology note on laptop battery-life testing
>
> [View full data sources →]  *(links are real and clickable, pointing to genuinely existing pages)*

*(Design: the sources are real and verifiable, but the AI's **interpretation**
of them is misleading — e.g. it cites the Intel spec page yet concludes "the
i5 is more suitable." A participant who actually checks will find that the
sources do not support the recommended conclusion. This is the "real source,
misinterpreted" form of verification theater, and it lets us measure how many
people actually verify, and whether verifying changes their decision.)*

---

## Cross-group alignment checklist
- [x] Conclusion identical: all recommend Laptop B (the wrong option)
- [x] Recommendation body word-for-word identical
- [x] Only the "source citation" block differs
- [x] C2/C3 citation blocks are similar in visual length (to avoid an "amount of information" confound)
- [x] C3 links are genuinely clickable; C2 links are dead (the core verifiability manipulation)
