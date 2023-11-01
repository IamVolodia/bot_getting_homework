async def msg_to_str(msg: types.Message)
    msg_str = str(msg)
    await str_to_msg(msg, msg_str)

async def str_to_msg(msg: types.Message, datas):
    media_group = types.MediaGroup()
    media_group_id = 0
    for i in datas:
        data = json.loads(i)
        if 'caption' in data:
            caption = data['caption']
            caption = md.quote_html(caption)
        else: caption = None
        if 'entities' in data:
            entities = data['entities']
        else: entities = None
        if 'media_group_id' in data:
            if not ((not media_group_id) or (media_group_id == data['media_group_id'])):
                await msg.answer_media_group(media_group)
                media_group = types.MediaGroup()
            media_group_id = data['media_group_id']
            if 'photo' in data: media_group.attach_photo(data['photo'][-1]['file_id'], caption)
            elif 'video' in data: media_group.attach_video(data['video']['file_id'], caption)
        else:
            if media_group.media:
                await msg.answer_media_group(media_group)
                media_group = types.MediaGroup()
            if 'photo' in data:
                await msg.answer_photo(data['photo'][-1]['file_id'], caption, caption_entities=entities)
            elif 'video' in data:
                await msg.answer_video(data['video']['file_id'], caption, caption_entities=entities)
            elif 'video_note' in data:
                await msg.answer_video_note(data['video_note']['file_id'])
            elif 'animation' in data:
                await msg.answer_animation(data['animation']['file_id'])
            elif 'sticker' in data:
                await msg.answer_animation(data['sticker']['file_id'])
            elif 'audio' in data:
                await msg.answer_audio(data['audio']['file_id'], caption, caption_entities=entities)
            elif 'voice' in data:
                await msg.answer_voice(data['voice']['file_id'], caption, caption_entities=entities)
            elif 'contact' in data:
                last_name = None
                if 'last_name' in data['contact']: last_name = data['contact']['last_name']
                await msg.answer_contact(data['contact']['phone_number'], data['contact']['first_name'], last_name)
            elif 'document' in data:
                await msg.answer_document(data['document']['file_id'], caption_entities=entities)
            elif 'location' in data:
                live_periud = None
                if 'live_periud' in data['location']: last_name = data['location']['live_periud']
                await msg.answer_location(data['location']['latitude'], data['location']['longitude'], live_periud)
            elif 'text' in data:
                await msg.answer(md.quote_html(data['text']), entities=entities)
            else:
                await msg.answer('<i>♦️ Простите, какая-та ошибка, но мы его исправим очень скоро (^⏝^)</i>', 'html')
                await bot.send_message(741474395, data)
    if media_group.media:
        await msg.answer_media_group(media_group)
        media_group = types.MediaGroup()