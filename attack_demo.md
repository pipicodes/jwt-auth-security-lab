# Attack Demonstration

## Project Summary
This lab demonstrates JWT authentication weaknesses caused by a weak signing secret and shows how forged tokens can lead to privilege escalation.

## Vulnerable Behavior
The vulnerable API uses a weak JWT secret:

`secret123`

An attacker who knows or guesses the secret can create their own token with elevated privileges.

## Attack Flow
1. Log in as a normal user
2. Observe that access to `/admin` is denied
3. Forge a new JWT with `role=admin`
4. Use the forged token to access `/admin`

## Impact
Privilege escalation through forged JWT tokens.

## Secure Behavior
The secure version improves the implementation by:
- using a stronger secret
- validating that the token role matches the server-side user record
- rejecting invalid or forged tokens

## Key Lesson
JWT security depends not only on token structure but also on strong secret management and server-side validation.