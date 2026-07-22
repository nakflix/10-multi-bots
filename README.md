<div align="center">
  <img src="https://telegra.ph/file/21034f4190632e5f571b0.jpg" width="600">
</div>

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=DC143C&center=true&lines=──+「+FILE+SENDER+」+──;An+Advanced+File+Sharing+Bot.&width=600&height=180">
</div>


### Features
 - Fully customizable.
 - Can be deployed on heroku & vps.
 - Customizable welcome message & Forcesub.
 - More than one post in one link (batch).
 - Flexible FSUB Button can be 1 button or 2 buttons or 3 buttons according to the var being filled.

### Setup

 - Add bot to Channel Database with all admin permissions
 - Add bot to Channel ForceSub add bot as ADMIN
 - Add bot to Group ForceSub add bot as ADMIN

### Running multiple bots (up to 10) from one deployment

This repo can run up to **10 independent bots** in a single deployment, each with
its **own bot token and its own MongoDB database**, while sharing the same
`OWNER_ID`, `CHANNEL_ID`, and `FORCE_SUB_CHANNEL_1-4` settings.

Copy `.env.example` for the full list of variables. The important part is the
per-bot block, repeated for as many bots as you want to run (leave a slot's
`BOT_TOKEN_<n>` unset to disable that slot):

```
BOT_NAME_1=Bot1
BOT_TOKEN_1=123456:AAA...        # from @BotFather
DATABASE_URL_1=mongodb+srv://.../  # this bot's own Mongo database
DATABASE_NAME_1=FileShareDB_1

BOT_NAME_2=Bot2
BOT_TOKEN_2=789012:BBB...
DATABASE_URL_2=mongodb+srv://.../
DATABASE_NAME_2=FileShareDB_2

... up to _10
```

Everything else (`OWNER_ID`, `CHANNEL_ID`, `FORCE_SUB_CHANNEL_1-4`, `ADMINS`,
messages, etc.) is set **once** and shared by every bot — no need to repeat it.

All bots run inside the same process and share a single web server for
health checks, so there is only ever one process bound to `$PORT` — this is
what avoids the "port is already in use" crash that happens if each bot
tries to bind its own web server to the same port.

Old single-bot deployments still work unchanged: if no `BOT_TOKEN_1..10` are
set, the app falls back to the classic `TG_BOT_TOKEN` / `DATABASE_URL` /
`DATABASE_NAME` variables.

### Deploy on Railway

1. Push/fork this repo to your own GitHub account.
2. On [Railway](https://railway.app), create a new project → **Deploy from GitHub repo**.
3. Railway will detect the `Dockerfile` and build from it automatically.
4. In the service's **Variables** tab, add the shared variables plus a
   `BOT_TOKEN_<n>` / `DATABASE_URL_<n>` pair for each bot you want to run
   (see `.env.example`).
5. Deploy. Railway injects `PORT` automatically — you don't need to set it.
   Check the deploy logs; you should see a `Bot Running..!` line for each
   configured bot, followed by one `Web server started on port ...` line.

<h3 align="center">
    『 ᴅᴇᴩʟᴏʏ ᴏɴ ʜᴇʀᴏᴋᴜ 』
</h3>

<p align="center"><a href="https://dashboard.heroku.com/new?template=https://github.com/Shauryanoobhai/FileShare"> <img src="https://img.shields.io/badge/Deploy%20On%20Heroku-black?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>


𝗡𝗢𝗧𝗘 :- 𝗙𝗢𝗥𝗞 𝗥𝗘𝗣𝗢 𝗕𝗘𝗙𝗢𝗥𝗘 𝗨𝗦𝗜𝗡𝗚 𝗔𝗡𝗗 𝗗𝗢𝗡'𝗧 𝗙𝗢𝗥𝗚𝗘𝗧 𝗧𝗢 𝗚𝗜𝗩𝗘 𝗦𝗧𝗔𝗥𝗦 😌 



<p align="center">
<a href="https://telegram.me/Ahjin_Sprt"><img src="https://img.shields.io/badge/-Support%20Group-blue.svg?style=for-the-badge&logo=Telegram"></a>
</p>
