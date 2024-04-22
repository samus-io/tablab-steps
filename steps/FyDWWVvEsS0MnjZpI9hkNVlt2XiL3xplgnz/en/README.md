# Horizontal Privilege Escalation

* Horizontal Privilege Escalation occurs when a user gains unauthorized access to resources or functionalities belonging to other users within the same privilege level.
* This type of vulnerability allows attackers to move laterally across the application's user base, accessing data or performing actions they are not authorized to perform.
* Let's break down different possible scenarios:
  * **Insecure Direct Object References (IDOR):**
    * IDOR vulnerabilities occur when an application fails to properly enforce access controls, allowing attackers to manipulate parameters or directly reference objects (such as database records or files) to access unauthorized data.
    * An attacker can modify a URL parameter to access another user's profile page or a sensitive data without proper authorization from database Or can use a hidden field in the submit form that allows to update user profile.
    * An attacker can access any kind of static files just by passing it to URL.

    ```js
        // Attacker can change userId=123 to userId=456
        https://example.com/profile?userId=123   
    
                                   OR
    
        <form action="/update_profile" method="post">
        <input type="hidden" name="user_id" value="456">
        <button type="submit">Update Profile</button>
        </form>
                                   OR    
    
      // Access to restricted Static file
      https://example.com/static/file.txt
    ```

  * **Location-based Access Control:**
    * Location-based access control restricts access to resources or functionalities based on the user's geographical location. However, if this control is improperly implemented, attackers can spoof their location or manipulate request headers to bypass these restrictions.
    * An attacker uses a VPN to spoof their location and access content restricted to a specific geographical location.
    * If server fails to identify the attacker location then it can cause exposure to location specific sensitive data.
  * **Referer-based Access Control:**
    * Referer-based access control restricts access to resources or functionalities based on the referring URL of the request.
    * Attackers can manipulate the Referer header to trick the application into granting access to unauthorized resources.
