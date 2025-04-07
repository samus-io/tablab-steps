# What is Cross-Site Request Forgery (CSRF)?

* `Cross-Site Request Forgery (CSRF)` is a web security vulnerability that tricks authenticated users into performing unintended actions on a trusted website.
* CSRF partially circumvents the `Same-Origin Policy (SOP)`, which is designed to isolate interactions between different websites. By leveraging the browser's implicit trust in the authenticated session, attackers can initiate malicious requests on behalf of the user.
* These attacks often originate from malicious websites, phishing emails, or embedded scripts, tricking a user's browser into sending undesired requests to a site where the user is authenticated. The targeted application cannot reliably identify the difference between a legitimate user request and one maliciously induced by an attacker.

  > :older_man: In a nutshell, the `Same-Origin Policy (SOP)` is a security feature in web browsers that restricts JavaScript running on one website from accessing or modifying content on another website with a different origin (composed of domain, protocol, and port).

## How it works

* The following diagram illustrates the workflow of a typical CSRF attack:

  ![CSRF workflow][1]

  1. The victim logs into a trusted website, which provides a session (e.g., a cookie) to their browser for authentication.
  1. The attacker crafts a malicious hyperlink that triggers an undesired action, such as modifying the victim's email (e.g., `https://vulnerable.tbl/change-email?newEmail=attacker@attacker.tbl`).
  1. The attacker delivers the malicious link through phishing emails, social engineering, or embedding it on a malicious website.
  1. The victim unknowingly clicks the link, initiating the attack.
  1. The victim's browser, still authenticated to the target website, automatically sends the forged request along with the session cookie, causing the trusted site to process it as legitimate and performing the unintended action.

## What could be achieved with CSRF

* Perform unintended actions within a trusted application on behalf of an authenticated user without their knowledge or consent, such as modifying account settings, changing passwords, updating email addresses, purchasing products, transferring funds, or altering security questions, leading to account takeover.
* Exploit CSRF to escalate privileges if combined with other vulnerabilities such as weak authentication mechanisms, or bypass specific access controls by making requests from the victim's authenticated session.
* Gain full access to the application's data, functionality, and critical configurations, potentially leading to a widespread compromise when leveraging a privileged user's session, such as an administrator's.

## XSS vs CSRF

* `Cross-Site Scripting (XSS)` and `Cross-Site Request Forgery (CSRF)` are separate security vulnerabilities with differing scopes and impacts:
  * XSS enables an attacker to run arbitrary JavaScript within the victim's browser, allowing full interaction with the web application as the user.
  * CSRF manipulates the victim into performing specific unintended actions, without granting the attacker direct control over the browser.
* The impact of XSS vulnerabilities is generally more severe than CSRF vulnerabilities:
  * The scope of CSRF attacks is usually constrained to certain subset of actions a user can perform, while XSS exploits often allow the attacker to perform any action available to the victim.
  * CSRF is categorized as a one-way attack because it only involves forging requests, without requiring access to responses, while XSS is considered as a two-way attack because the injected script can send arbitrary requests, process responses, and exfiltrate data to an attacker-controlled domain.

[1]: /static/images/csrf-workflow.png
