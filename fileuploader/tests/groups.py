import fileuploader
import asyncio


async def run():
    user = await fileuploader.User.login("Username", "Password")  # Log in into an account
    new_group = await user.create_group("New group")  # Create new group
    print(new_group)

    groups = await user.get_groups()  # Get list of all groups
    print(groups)

    invite_link = await groups[-1].generate_invite(user=user)  # Generate invite link to an account
    print(invite_link.link_full)  # Get full invite link

    await groups[-1].leave(user=user)  # Leave from a group

    invite_link_info = await invite_link.info(user=user)  # Get info about invite link
    print(invite_link_info)

    invited_group = await invite_link.join(user=user)  # Join to the group
    print(invited_group)


asyncio.run(run())
