# What is Cross-Site Request Forgery (CSRF)?

* Cross-Site Request Forgery (CSRF) is a web security vulnerability that tricks authenticated users into performing unintended actions on a trusted website.
* CSRF partially circumvents the Same-Origin Policy (SOP), which is designed to isolate interactions between different websites. By leveraging the browser's implicit trust in the authenticated session, attackers can initiate malicious requests on behalf of the user.
* These attacks often originate from malicious websites, phishing emails, or embedded scripts, tricking a user's browser into sending unauthorized requests to a site where the user is authenticated.
* The targeted application cannot differentiate between a legitimate request and the forged request initiated by the attacker.

> :older_man: The Same-Origin Policy (SOP) is a security mechanism implemented in web browsers to restrict how documents or scripts from one origin (domain, protocol, and port) can interact with resources from another origin.

## How it works

* The following diagram illustrates the workflow of a typical CSRF attack:

![CSRF workflow][1]

1. The victim logs into a website, which assigns a session token (e.g., a cookie) to their browser for authentication.
1. The attacker creates a malicious hyperlink that triggers an unauthorized action (e.g., changing the victim's password).
1. The attacker delivers the malicious link through phishing emails, social engineering, or embedding it on a malicious website.
1. The victim unknowingly clicks the link, initiating the attack.
1. The victim's browser, still authenticated to the target website, automatically sends the forged request. The website processes the request as if it were legitimate, performing the unintended action.

## What could be achieved with CSRF?

* A successful CSRF attack forces the victim to perform unintended actions on a trusted application.
* For example, this might be to change the email address on their account, to change their password, or to make a funds transfer. Depending on the nature of the action, the attacker might be able to gain full control over the user's account.
* If the attacker exploits a privileged user's session (e.g., an administrator), they could gain full control over the application's data, functionality, or sensitive configurations, potentially leading to widespread compromise.

## XSS vs CSRF

* Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) are distinct vulnerabilities that differ in scope and impact:
  * XSS allows an attacker to execute arbitrary JavaScript in the victim's browser, enabling full interaction with the web application on the user's behalf.
  * CSRF manipulates the victim into performing specific actions they did not intend, without the attacker gaining direct control of the browser.
* While both are serious vulnerabilities, XSS is generally more severe because it:
  * CSRF typically affects a limited subset of actions a user can perform, while XSS exploits often allow the attacker to perform any action available to the victim.
  * CSRF is a "one-way" vulnerability: the attacker can induce requests but cannot see the responses. In contrast, XSS is "two-way," allowing attackers to read responses, execute additional requests, and exfiltrate data.

[1]: /static/images/csrf-workflow.png