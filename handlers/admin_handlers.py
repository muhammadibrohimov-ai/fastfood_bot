from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .buttons import admin_kb, registered_kb, add_foods, inline_keyboard_foods, order_show, order_inline_kb

from database import add_to_table, get_order_food, change_table, get_foods, get_comments

from environs import Env
env = Env()
env.read_env()

ADMIN_ID = env.str("ADMIN")

admin_router = Router()

class Register_food(StatesGroup):
    name = State()
    image = State()
    decription = State()
    price = State()
    quantity = State()
    
class Edit_food(StatesGroup):
    feature = State()


@admin_router.message(F.text == "Admin panelga o'tish")
@admin_router.message(Command("admin"))
async def start_admin(message:Message):
    id = str(message.from_user.id)
    if str(ADMIN_ID) == id:
        await message.answer(
            text = 
            "🎛 <b>Admin Panel</b> ga xush kelibsiz!\n\n"
        "Quyidagi bo‘limlardan birini tanlang:\n\n"
        "🍽 Taomlar\n"
        "🛒 Buyurtmalar\n"
        "💬 Xabarlar\n"
        "👤 User panelga qaytish",
            reply_markup=admin_kb
        )
    else:
        await message.answer(
            text = "Siz 🎛admin emasssiz, iltimos kerakli tugmani tanlang: ",
            reply_markup=registered_kb
        )
        
@admin_router.message(F.text == 'Taomlar')
async def add_food(message:Message):
        await message.answer(
            text = "Quyidagilardan birini tanlang: ",
            reply_markup=add_foods
        )
    
@admin_router.callback_query(F.data.startswith('new'))
async def choose_which(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Register_food.name)
    await callback.message.answer(
            text = "Taom nomini kiring: "
        )
    callback.answer()
        
        

@admin_router.message(Register_food.name)
async def get_new_food_name(message:Message, state:FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Register_food.image)    
    await message.answer(
        text = "Iltimos taomning rasmini jo'nating"
    )
    
@admin_router.message(Register_food.image)
async def get_new_food_image(message:Message, state:FSMContext):
    if not message.photo:
        await message.answer(
            text = "Iltimos taomning qayta rasmini jo'nating"
        ) 
    
    else:
        photo_id = message.photo[-1].file_id
        await state.update_data(image = photo_id)
        await state.set_state(Register_food.decription)
        await message.answer(
            text = f'{photo_id}\nIltimos taomga sharh yozing: '
        )
        
@admin_router.message(Register_food.decription)
async def get_description(message:Message, state:FSMContext):
    text = message.text
    await state.update_data(description = text)
    await state.set_state(Register_food.price)
    await message.answer("Iltimos taomning narxini kiritng: ")
        
@admin_router.message(Register_food.price)
async def get_new_food_price(message:Message, state:FSMContext):
    await state.update_data(price = message.text)
    await state.set_state(Register_food.quantity)
    await message.answer(
        text = 'Iltimos taomning miqdorini kiritng: '
    )
    

@admin_router.message(Register_food.quantity)
async def get_new_food_quantity(message:Message, state:FSMContext):
    await state.update_data(quantity = message.text)
    data = await state.get_data()
    await state.clear()
    if add_to_table('foods', name = data['name'], price = data['price'], image = data['image'], quantity = data['quantity'], description = data['description']):
        await message.answer(
            text = f"Taom database ga qo'shildi!\n{data}",
            reply_markup=admin_kb
        )
        
    else:
        await message.answer(
            text = "Xatolik ketdi qayta urining\nQuyidagilardan birini tanlang: ",
            reply_markup=add_foods
        )
        
        
        
@admin_router.callback_query(F.data == "existing_food")
async def start_editing_food(callback:CallbackQuery, state:FSMContext):
    
    await callback.answer(
        text = "Siz uchun kerakli bo'lgan taomning kerakli narsanini o'zgartiring: "
    )
    
    
    
    if get_foods():
        for food in get_foods():
            text = (
                f"🍽 Taom: {food[1]}\n"
                f"💵 Narxi: {food[3]} so'm\n"
                f"📦 Mavjud: {food[4]} ta\n"
                f"ℹ️ Tavsif: {food[5]}"
            )
            await callback.message.answer_photo(
                photo=food[2],
                caption=text,
                reply_markup = await inline_keyboard_foods(food[0])
            )
            
    else:
        await callback.message.answer(
            text = 'Afsuski hozirda taom mavjud emas!\nIltimos yangi taom qoshing',
            reply_markup=add_foods
        )
        
        
@admin_router.callback_query(F.data.startswith("edit"))
async def edit_food_by_feature(callback:CallbackQuery, state:FSMContext):
    await state.set_state(Edit_food.feature)
    
    features = ['name', 'price', 'image', 'quantity', 'description',"❌Delete"]
    
    feature = callback.data.split("_")[2]
    food_id = callback.data.split("_")[1]
        
    if features[int(feature)] == "❌Delete":
        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.edit_caption(
            caption="Ushbu taom muvaffaqiyatli o'chirildi!!!"
        )

        change_table(f"DELETE FROM foods WHERE id = {food_id}")

        await state.clear()
        
    else:
        await state.update_data(food_id = food_id)
        
        await state.update_data(feature  = features[int(feature)])
        
        await callback.message.edit_reply_markup(reply_markup=None)

        await callback.message.edit_caption(
            caption=f"{features[int(feature)]} ni yangi qiymatini kiritng: "
        )


@admin_router.message(Edit_food.feature)
async def get_feature(message:Message, state:FSMContext):
    value = message.text
    await state.update_data(value = value)
    data = await state.get_data()
    
    await state.clear()
    
    query = f"UPDATE foods SET {data['feature']}={data['value']} WHERE id={data['food_id']};" if data['feature'] not in ['image', 'name', 'description'] else f"UPDATE foods SET {data['feature']}='{data['value']}' WHERE id={data['food_id']};"
    
    change_table(query)
    
    await message.answer(
        text = "O'zgardi",
        reply_markup=admin_kb
    )
    


@admin_router.message(F.text == 'Back')
async def get_back(message:Message):
    await message.answer(
        text = "Admin oanelning asosiy oynasihga qaytdingiz!\n",
        reply_markup=admin_kb
    )


        
@admin_router.message(F.text == "Buyurtmalar")
async def show_orders(message:Message):
    await message.answer(
        text = 'Qanday turdagi buyurtmalarni ko\'rmoqchisiz, kerakli tugmani bosing: ',
        reply_markup=order_show
    )
    
    
@admin_router.message(F.text == "🆕New")
async def show_new_order(message:Message):
    foods = get_order_food(status='new')
    if foods:
        for i in foods:
            order_id, food_name, user_id, food_price, order_quantity, total_price = i
            await message.answer(
                text = f'🍽 Taom: {food_name}\n💵 Narxi: {food_price:,} so\'m\n📦 Soni: {order_quantity}\n💵 Umumiy: {total_price:,} so\'m\n',
                reply_markup=await order_inline_kb(order_id)
            )    
            
    else:
        await message.answer(
            text = "Afsuski bunday turdagi buyurtmalar mavjud emas!!",
            reply_markup=admin_kb
        )
        
@admin_router.message(F.text == "In progress")
async def show_progress_order(message:Message):
    foods = get_order_food(status='in_progress')
    if foods: 
        for i in foods:
            order_id, food_name, user_id, food_price, order_quantity, total_price = i
            await message.answer(
                text = f'🍽 Taom: {food_name}\n💵 Narxi: {food_price:,} so\'m\n📦 Soni: {order_quantity}\n💵 Umumiy: {total_price:,} so\'m\n',
                reply_markup=await order_inline_kb(order_id, 2)
            )  
            
    else:
        await message.answer(
            text = "Afsuski bunday turdagi buyurtmalar mavjud emas!!",
            reply_markup=admin_kb
        )  
            
@admin_router.message(F.text == "Finished")
async def show_progress_order(message:Message):
    foods = get_order_food(status='finished')
    
    if foods:
        for i in foods:
            order_id, food_name, user_id, food_price, order_quantity, total_price = i
            await message.answer(
                text = f'🍽 Taom: {food_name}\n💵 Narxi: {food_price:,} so\'m\n📦 Soni: {order_quantity}\n💵 Umumiy: {total_price:,} so\'m\n',
                reply_markup=await order_inline_kb(order_id, 2)
            )    
        
    else:
        await message.answer(
            text = "Afsuski bunday turdagi buyurtmalar mavjud emas!!",
            reply_markup=admin_kb
        )

@admin_router.callback_query(F.data.startswith(('progress', 'finish')))
async def change_order(callback:CallbackQuery):
    status = callback.data.split('_')[0]
    order_id = callback.data.split('_')[1]
    print(order_id)
    if change_table("UPDATE orders SET status = '%s' WHERE id = %s"%('finished' if status == 'finish' else 'in_progress', order_id)):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text = 'Success')
        
@admin_router.callback_query(F.data.startswith('cancel'))
async def change_order(callback:CallbackQuery):
    status = callback.data.split('_')[0]
    order_id = callback.data.split('_')[1]
    print(order_id)
    if change_table(f"UPDATE orders SET status = '{status}' WHERE id = {order_id}"):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text = 'Success')
        
        
@admin_router.message(F.text == "Xabarlar")
async def show_comments(message: Message):
    comments = get_comments()
    if not comments:
        await message.answer("❌ Hali izohlar yo‘q", reply_markup=admin_kb)
        return
    
    for row in comments:
        comment_id, chat_id, comment, created_at = row
        
        text = (
            f"🆔 {comment_id}\n"
            f"👤 Chat ID: {chat_id}\n"
            f"💬 Izoh:\n\n{comment}\n\n"
            f"📅 Sana: {created_at}\n\n"
        )
        
        await message.answer(text, reply_markup=admin_kb)

        

        

    
