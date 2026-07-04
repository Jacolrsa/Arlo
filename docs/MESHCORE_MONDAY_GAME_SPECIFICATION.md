# MeshCore Monday Game Specification

## MeshCore Monday v1.0

## Purpose

MeshCore Monday encourages users to get active on the MeshCore network every Monday.

The game must be simple, reliable, deterministic, and suitable for hundreds or thousands of users.

The public channel must remain clean.

This document is authoritative. Future MeshCore Monday code must follow this specification exactly.

---

## Command

The command is:

```text
#meshcoremonday
```

The command is case-insensitive.

The following examples are all valid:

```text
#meshcoremonday
#MeshCoreMonday
#MESHCOREMONDAY
```

The command is intended to be sent in the public MeshCore Monday channel.

---

## Monday Eligibility

Only Monday check-ins are accepted.

Monday is determined using the Home Assistant local timezone.

Monday begins at:

```text
00:00
```

Monday ends at:

```text
23:59:59
```

If it is not Monday:

- Arlo must not log a check-in.
- Arlo must not reply.
- Arlo must not update statistics.
- Arlo must silently ignore the command.

---

## Player Identity

Player identity is the MeshCore public key.

Display names may change.

All statistics remain attached to the MeshCore public key.

---

## Check-In Rule

Each player may check in only once per Monday.

If a player attempts another check-in during the same Monday:

- Arlo must not reply.
- Arlo must not log another check-in.
- Arlo must not update statistics.
- Arlo must silently ignore the duplicate command.

---

## Valid Check-In Public Response

For a valid check-in, Arlo posts exactly one public message:

```text
📟 <PlayerName> checked in.

You are #<position> this week.
```

No further public messages are permitted for that check-in.

The public channel must remain clean.

Only the single public acknowledgement is permitted.

---

## Valid Check-In Direct Message

Immediately after the public message, Arlo sends exactly one direct message to the player.

The direct message must follow this format:

```text
📟 Welcome back <PlayerName>!

✅ Week <WeekNumber> check-in complete.

🔥 Current streak: <CurrentStreak> weeks

📅 Total check-ins: <TotalCheckins>
```

Nothing else is sent.

The MeshCore Monday v1.0 flow must not include:

- Questions.
- AI conversation.
- Menus.
- Additional prompts.
- Additional direct messages.

---

## Player Statistics

Player statistics consist of:

- Public Key
- Display Name
- First Check-in
- Last Check-in
- Current Streak
- Longest Streak
- Total Check-ins

---

## Weekly Statistics

Weekly statistics consist of:

- Year
- ISO Week Number
- Total Check-ins
- Order of Check-ins

The check-in position shown in the public response is determined by the weekly order of successful check-ins.

---

## Streak Rules

Current streak increases by one if the previous successful check-in occurred during the previous Monday.

If one or more Mondays are missed:

- Current streak becomes 1 on the next valid check-in.

Longest streak never decreases.

---

## Weekly Summary

Every Tuesday at 07:00 using Home Assistant local time, Arlo automatically posts one weekly summary.

The summary must follow this format:

```text
📟 MeshCore Monday Results

48 members checked in this week.

🥇 First 5

1.
2.
3.
4.
5.

🔥 Top 5 Streaks

1.
2.
3.
4.
5.

See you next Monday!
```

The summary is generated only once per week.

If Home Assistant was offline at 07:00, the summary should be generated once after startup if it has not already been posted.

---

## Reliability Requirements

The implementation must prioritize:

- Reliability
- Simplicity
- Deterministic behaviour
- No duplicate rewards
- No duplicate check-ins
- No unnecessary conversation

---

## Non-Goals for v1.0

MeshCore Monday v1.0 must not include:

- XP
- Levels
- Badges
- Achievements
- Titles
- Menus
- Questions
- AI conversation
- Mini-games
- Multiple direct messages
- Public conversation beyond the required acknowledgement and weekly summary

These features may be designed for future versions, but they are not part of this official v1.0 specification.

---

## Version History

### v1.0

Initial official MeshCore Monday specification.
