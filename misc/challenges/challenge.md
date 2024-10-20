## Some of the interesting challenges

    1. When I ran the server no my PC (Linux) at home on OCT 19 it ran perfectly, but when I ran it the next day the server crashed, the issue turned out to be a problem with Windows text formating, the solution was opening a file usiong utf8 format, What crashed the system was the inclusion of an emoji "❤️", love crashed the server!.

    2. There was a funny CSS bug I used "flexbox" instead of "flex" in display: property.

    3. I needed to do frequent changes to the DateBase Schema, so the CRUD crashed frequently, so solve this I used SQLAlchemy's Alembic library, which automate schema changes, a real life-saver.

    4. I needed to scale down the project