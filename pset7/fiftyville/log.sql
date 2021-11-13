-- Keep a log of any SQL queries you execute as you solve the mystery.
sqlite3 fiftyville.db
.schema


SELECT description FROM crime_scene_reports WHERE year=2020 AND month=7 AND day=28 AND street="Chamberlin Street";
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

SELECT name, transcript FROM interviews WHERE id IN (SELECT id FROM crime_scene_reports WHERE year=2020 AND month=7 AND day=28 AND street="Chamberlin Street");
-- FAILED OBVIOSLY NOT SHARED IDs

SELECT name, transcript FROM interviews WHERE year=2020 AND month=7 AND day=28;
--Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
--Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
--Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


SELECT hour, activity, license_plate FROM courthouse_security_logs WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND 15<minute AND minute<25;
-- 10 | exit | 5P2BI95
-- 10 | exit | 94KL13X
-- 10 | exit | 6P58WS2
-- 10 | exit | 4328GD8
-- 10 | exit | G412CB7
-- 10 | exit | L93JTIZ
-- 10 | exit | 322W7JE
-- 10 | exit | 0NTHK55

SELECT name, passport_number, license_plate, atm_transactions.transaction_type, atm_transactions.atm_location FROM people JOIN bank_accounts ON people.id=bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number=atm_transactions.account_number WHERE year=2020 AND month=7 AND day=28 AND atm_location LIKE "%fifer street%" AND transaction_type LIKE "%withdraw%";
--Ernest | 5773159633 | 94KL13X | withdraw | Fifer Street
--Russell | 3592750733 | 322W7JE | withdraw | Fifer Street
--Roy | 4408372428 | QX4YZN3 | withdraw | Fifer Street
--Bobby | 9878712108 | 30G67EN | withdraw | Fifer Street
--Elizabeth | 7049073643 | L93JTIZ | withdraw | Fifer Street
--Danielle | 8496433585 | 4328GD8 | withdraw | Fifer Street
--Madison | 1988161715 | 1106N58 | withdraw | Fifer Street
--Victoria | 9586786673 | 8X428L0 | withdraw | Fifer Street

SELECT name, passport_number, license_plate, FROM people JOIN bank_accounts ON people.id=bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number=atm_transactions.account_number WHERE year=2020 AND month=7 AND day=28 AND atm_location LIKE "%fifer street%" AND transaction_type LIKE "%withdraw%" AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND 15<minute AND minute<25);
--Ernest | 5773159633 | 94KL13X
--Russell | 3592750733 | 322W7JE
--Elizabeth | 7049073643 | L93JTIZ
--Danielle | 8496433585 | 4328GD8

SELECT people.name, phone_calls.receiver FROM people JOIN phone_calls ON people.phone_number=phone_calls.caller WHERE phone_calls.year=2020 AND phone_calls.month=7 AND phone_calls.day=28 AND phone_calls.duration<60 and people.name IN (SELECT name FROM people JOIN bank_accounts ON people.id=bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number=atm_transactions.account_number WHERE year=2020 AND month=7 AND day=28 AND atm_location LIKE "%fifer street%" AND transaction_type LIKE "%withdraw%" AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND 15<minute AND minute<25));
--Ernest | (375) 555-8161
--Russell | (725) 555-3243

SELECT people.name, flights.destination_airport_id, flights.hour, flights.minute FROM people JOIN passengers ON passengers.passport_number=people.passport_number JOIN flights ON passengers.flight_id=flights.id JOIN airports ON flights.origin_airport_id=airports.id WHERE flights.year=2020 AND flights.month=7 and flights.day=29 AND passengers.passport_number IN (SELECT people.passport_number FROM people JOIN phone_calls ON people.phone_number=phone_calls.caller WHERE phone_calls.year=2020 AND phone_calls.month=7 AND phone_calls.day=28 AND phone_calls.duration<60 and people.name IN (SELECT name FROM people JOIN bank_accounts ON people.id=bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number=atm_transactions.account_number WHERE year=2020 AND month=7 AND day=28 AND atm_location LIKE "%fifer street%" AND transaction_type LIKE "%withdraw%" AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year=2020 AND month=7 AND day=28 AND hour=10 AND 15<minute AND minute<25)));
-- Russell | 6 | 16 | 0
-- Ernest | 4 | 8 | 20



SELECT flights.hour, flights.minute FROM flights JOIN airports ON airports.id=flights.origin_airport_id WHERE flights.year=2020 AND flights.month=7 and flights.day=29 AND flights.hour<9 AND airports.city LIKE "%fiftyville%" ORDER BY hour, minute;

-- 8 | 20

 --ERNEST DID IT! EARLIEST FLIGHT

SELECT city FROM airports WHERE id=4;
--London
-- HE WENT TO LONDON

SELECT name FROM people WHERE phone_number="(375) 555-8161";
-- Berthold helpped him