# Broken playbook (initial)
- name: Broken playbook
  hosts: webservers
  become: yes
  vars:
    page_title: "Hello World"
  tasks:
    - name: Install_apache
      dnf_install:
        name: httpd
        state: present

    - name: Deploy and index.html file
      copy:
        content: "{{ page_title }}"
        dest: /var/www/html/index.html

    - name: Activate httpd
      service:
        name: apache2
        state: started

    - name: Add a line to index.html
      lineinfile:
        path: /var/www/html.index.html
        line: "Edited by ansible"
        state: present
```

I used a prompt like:
"This is an Ansible playbook with problems during execution. Please identify the issues and fix all possible problems."

Here’s the ChatGPT interface I used (for context):

<Frame>
  <img alt="A screenshot of the ChatGPT webpage with the central prompt &#x22;What's on your mind today?&#x22; and a typed message mentioning an Ansible playbook. Browser tabs and a Red Hat-themed toolbar are visible along the top." />
</Frame>

## Common issues found

ChatGPT identified the following key problems and recommended fixes. The table below summarizes each issue and what to change.

| Problem                                        | Why it fails                                                 | Recommended fix                                                 |
| ---------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| Nonexistent module name `dnf_install`          | Not an Ansible module — causes module not found              | Use `ansible.builtin.dnf` (FQCN preferred) or `dnf`             |
| Wrong service name `apache2` on RHEL/CentOS    | RHEL uses `httpd` service name                               | Use `httpd` for service operations                              |
| Incorrect file path `/var/www/html.index.html` | Typo — invalid path                                          | Correct to `/var/www/html/index.html`                           |
| Inconsistent become values                     | `become: yes` is okay, but use `become: true` consistently   | Use `become: true` at play or task level                        |
| Linting/compliance                             | Not using FQCNs and missing file ownership/permissions       | Use `ansible.builtin.*`, set `owner`, `group`, `mode` as needed |
| Handler notifications mismatch                 | notify name must match handler name exactly (case-sensitive) | Define handler matching notify string                           |

Other best practices: ensure you run playbooks against test hosts, verify OS/distribution, and set correct file ownership for web content.

## Fixed playbook

After iterating with ChatGPT, incorporating the correct context (RHEL target, need for privilege escalation, best practices), we consolidated a single corrected playbook. It uses FQCNs, `become: true`, correct service/module names, and properly configured handlers.

```yaml theme={null}
---
- name: Install and configure Apache on RHEL systems
  hosts: webservers
  become: true  # Elevated privileges for tasks that require it
  vars:
    page_title: "Hello from Ansible Best Practices"

  tasks:
    - name: Ensure Apache is installed
      ansible.builtin.dnf:
        name: httpd
        state: present
      notify: restart apache

    - name: Deploy index.html file
      ansible.builtin.copy:
        content: "<html><body><h1>{{ page_title }}</h1></body></html>"
        dest: /var/www/html/index.html
        owner: apache
        group: apache
        mode: '0644'
      notify: restart apache

    - name: Ensure Apache service is running and enabled
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: true

    - name: Add a line to index.html
      ansible.builtin.lineinfile:
        path: /var/www/html/index.html
        line: "Edited by Ansible"
        state: present
        insertafter: EOF
      notify: restart apache

  handlers:
    - name: restart apache
      ansible.builtin.service:
        name: httpd
        state: restarted
```

<Callout icon="lightbulb">
  Always verify the environment (OS/distribution), service names, and file ownership before applying changes to production systems. Run playbooks against a non-production or test host first.
</Callout>

## Run the corrected playbook

Save the fixed file as `site.yml`, then execute it with `ansible-playbook`:

```bash theme={null}
student@control:~/buggy$ ansible-playbook /home/student/buggy/site.yml
```

Expected (successful) output:

```text theme={null}
TASK [Ensure Apache is installed] *************************************************
ok: [servera]

TASK [Deploy index.html file] *****************************************************
changed: [servera]

TASK [Ensure Apache service is running and enabled] *******************************
ok: [servera]

TASK [Add a line to index.html] ***************************************************
changed: [servera]

RUNNING HANDLER [restart apache] **************************************************
changed: [servera]

PLAY RECAP *********************************************************************
servera                   : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Conclusion

Iteratively feeding real error output and context to ChatGPT can speed up diagnosing and fixing broken playbooks. Key takeaways:

* Provide correct context up front (OS distribution, required privileges, intended service names).
* Prefer FQCNs (ansible.builtin.\*) to satisfy linters and avoid ambiguity.
* Test playbooks on non-production hosts before rolling out changes.
* Human review remains essential: validate generated changes and verify ownership/permissions.

## Links and References

* [Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)
* [VS Code](https://code.visualstudio.com/)
* [ChatGPT](https://chat.openai.com/)

Further reading:

* Ansible module index and FQCN guidance in official docs
* Best practices for handlers and notifications

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/68946e8d-b927-4205-8f24-67bfb2019cf2/lesson/ed5eaddc-ea4f-435e-9319-593c10012224" />
</CardGroup>


# Playbook Generation Using Prompts

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Using-ChatGPT-With-Ansible/Playbook-Generation-Using-Prompts/page

Guide to generating Ansible playbooks from natural language prompts, prompt engineering techniques, templates, validation checklist and best practices for safe, idempotent AI-assisted playbook creation.

În această lecție explicăm cum poți genera playbook-uri Ansible direct din instrucțiuni în limbaj natural. În loc să scrii manual YAML, descrii în clar ce vrei să automatizezi, iar modelul generează structura YAML gata de utilizare.

Modelele moderne (de exemplu ChatGPT, în configurații adecvate) pot produce playbook-uri complete pornind doar de la instrucțiuni textuale. Astfel nu mai este necesar să reții fiecare detaliu sintactic: te concentrezi pe ce vrei să automatizezi, iar modelul traduce acel intent în YAML. Totuși, calitatea promptului tău influențează direct calitatea playbook-ului rezultat.

<Frame>
  <img alt="A slide titled &#x22;Automating with ChatGPT&#x22; showing a flow from a &#x22;Plain English prompt&#x22; through the ChatGPT logo to a &#x22;Ready-to-use YAML playbook.&#x22; The caption reads, &#x22;No need to memorize syntax—ChatGPT structures it for you.&#x22;" />
</Frame>

Sarcini simple, cum ar fi instalarea Apache, sunt ușor de generat. Pentru cerințe mai complexe — de exemplu: configurarea Apache ca web server, definirea unui serviciu, servirea unei pagini index.html personalizate — structura playbook-ului și modulele alese se schimbă. De aceea contează claritatea și detalierea instrucțiunii.

<Frame>
  <img alt="A slide titled &#x22;Why Prompt Engineering Matters&#x22; that compares two chat examples: on the left a short prompt &#x22;install Apache&#x22; labeled &#x22;Small basic playbook,&#x22; and on the right a more detailed prompt &#x22;configure Apache as a web server with a custom homepage&#x22; labeled &#x22;Detailed structured playbook.&#x22;" />
</Frame>

Un prompt bine formulat reduce riscul erorilor de sintaxă, alegerea incorectă a modulelor sau parametrii nepotriviți, iar playbook-ul generat va fi ușor de adaptat.

<Frame>
  <img alt="A presentation slide titled &#x22;Why Prompt Engineering Matters&#x22; showing four numbered boxes. They list benefits: adds context and clarity, ensures correct modules and parameters, reduces syntax errors and rework, and generates near-ready playbooks with minimal edits." />
</Frame>

Cum construiești un prompt eficient

* O formulare bună are patru părți principale: Obiectiv, Mediul, Detaliile și Practici recomandate. Include aceste elemente pentru a transforma o solicitare vagă într-un request structurată și util.

Tabel: Structura recomandată a unui prompt

| Element              | Ce să incluzi                                                  | Exemplu de formulare                                                                                                 |
| -------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Obiectiv             | Ce vrei să obții în termeni de stare dorită (nu pași)          | "Creează un playbook care instalează Apache, pornește serviciul și servește o pagină index.html personalizată."      |
| Mediul               | OS/tintă/host group, modul de gestionare pachete (apt/yum)     | "Target: Ubuntu 22.04, inventar: group `webservers`."                                                                |
| Detaliile            | Versiuni, variabile, conținut fișiere, porturi, utilizatori    | "Apache 2.4, pagina index include banner cu numele mediului, port 8080."                                             |
| Practici recomandate | Cerințe de idempotenta, module native, handlers, nume task-uri | "Folosește `apt`/`service`/`template`, evită `shell` când există un modul dedicat; include handlers pentru restart." |

Model de prompt (șablon) — poți adapta la nevoile tale:

```YAML theme={null}
Act as an experienced DevOps engineer who follows Ansible best practices.
Goal: Create an Ansible playbook to install and configure Apache to serve a custom index.html.
Environment: Target group "webservers" on Ubuntu 22.04.
Details: Install apache2, ensure service is enabled and started, deploy /var/www/html/index.html with a banner "ENV: staging", listen on port 8080.
Best practices: Use native Ansible modules (apt, service, template), idempotent tasks, handlers for service restart, clear task names.
Return: Full YAML playbook only, no extra commentary.
```

<Frame>
  <img alt="An infographic titled &#x22;Structure of a Good Request&#x22; with four colorful circular icons. Each icon is labeled Goal, Environment, Details, and Best Practices, giving short tips like state what you want, mention OS/target, specify versions, and remind the AI to follow standards." />
</Frame>

Tehnici avansate de prompting

* Prompturi contextuale — Include background: arhitectură, limitări de securitate, roluri utilizatori, proxy/firewall necesar.
* Rafinare iterativă — Cere revizuiri: "Arată-mi varianta cu handlers, apoi o versiune fără handlers." Iterează până la variantă optimă.
* Concentrează-te pe stare dorită — Spune ce rezultat aștepți (ex.: "index.html prezent și servit la /"), nu cum să ajungă acolo.
* Atribuie rol modelului — "Acționează ca un inginer DevOps senior" ajută modelul să aplice bune practici.

<Frame>
  <img alt="A presentation slide titled &#x22;Advanced Techniques&#x22; showing four numbered prompt-engineering tips: Contextual Prompts, Iterative Refinement, Desired State Focus, and Assign a Role, each with a brief explanation. The layout uses a dark blue background with colored accents above each column." />
</Frame>

Evaluare înainte de execuție — checklist esențial
După generarea playbook-ului este crucial să îl validezi manual. Modelele accelerează scrierea, dar responsabilitatea verificării rămâne la tine.

Tabel: Checklist de evaluare

| Verificare        | Ce să verifici                                                         | Instrumente utile                  |
| ----------------- | ---------------------------------------------------------------------- | ---------------------------------- |
| Sintaxă YAML      | Indentare corectă, valid YAML                                          | yamllint, ansible-lint             |
| Platformă         | Module compatibile cu OS-ul țintă (apt vs yum vs win\_feature)         | Documentația Ansible, test pe VM   |
| Parametri/Opțiuni | Verifică dacă parametrii există și nu sunt depricați                   | Ansible docs: module reference     |
| Logică & Flux     | Ordinea task-urilor, handlers notificate, condiții `when`, idempotenta | Execuție în `--check`, peer review |

<Frame>
  <img alt="A presentation slide titled &#x22;Evaluate Before You Run&#x22; that lists four checklist items: Syntax, Platform, Options, and Logic. Each item has a short note (e.g., check YAML structure, verify module compatibility, validate parameters, review task flow)." />
</Frame>

<Callout icon="warning">
  Rulați playbook-urile generate întâi într-un mediu de test/staging. Folosiți opțiuni precum --check și --diff când este posibil și efectuați un run controlat înainte de a le rula în producție.
</Callout>

După validare în mediu de test, poți aplica playbook-ul în producție având un risc mult mai mic. Reține: AI-ul oferă un punct de plecare puternic, dar responsabilitatea finală pentru corectitudine, securitate și compatibilitate este a ta.

Links și referințe utile

* [Ansible Documentation — Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
* [Ansible Module Index](https://docs.ansible.com/ansible/latest/collections/index_module.html)
* [YAML Lint (yamllint)](https://yamllint.readthedocs.io/)
* [Ansible Lint (ansible-lint)](https://ansible-lint.readthedocs.io/)
* [OpenAI / ChatGPT](https://openai.com/) — pentru referințe despre modele conversationale

Cuvinte cheie SEO: Ansible playbook, generare playbook cu AI, prompt engineering pentru Ansible, ChatGPT Ansible, bune practici Ansible, idempotenta, ansible-lint.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/68946e8d-b927-4205-8f24-67bfb2019cf2/lesson/abc4e556-1816-4456-90bd-bc8c585afbd2" />
</CardGroup>
