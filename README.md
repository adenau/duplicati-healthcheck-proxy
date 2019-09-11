# duplicati-healthcheck-proxy

Duplicati (found at ...) is an excellent backup solution, but can be challenging to manage when installed on a large number of computers. There are some excellent centralized monitoring solution, such as . However, I am currently using Heathchecks.io (found at https://healthchecks.io) to monitor my infrastructure. As such, I needed a solution to link both products.

## The Solution

Heathchecks.io is a cron monitoring solution : it allows you to monitor that your repetitive jobs are executing at their regular schedule. With a little tweaking, the product can also be used as fully-fledge monitoring product.

Duplicati is a backup software that can be installed on most modern desktop OS (Windows, Mac, Linux, etc.) and some NAS devices. It is my favored backup product because it allows for multiple destination and offers a Web management system. When backups are completed, it can send a report to a specific URL.
