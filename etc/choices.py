USER_ROLES = (
    ('admin', 'مدير'),
    ('doctor', 'دكتور'),
    ('receptionist', 'استقبال'),
    ('patient', 'مريض'),
)

GENDER_CHOICES = (
    ('male', 'ذكر'),
    ('female', 'انثى'),
)

EXAMINATION_TYPE_CHOICES = (
    ('time_share', 'تقاسم الوقت'),
    ('percentage', 'نسبة مئوية'),
)

APPOINTMENT_STATUS_CHOICES = (
    ('pending', 'قيد الانتظار'),
    ('completed', 'تم الكشف'),
    ('confirmed', 'تم التأكيد'),
    ('cancelled', 'تم الإلغاء'),
)

CONCENTRATION_UNIT_CHOICES = (
    ('mg', 'ملجم'),
    ('mcg', 'مكجم'),
    ('mg/ml', 'ملجم/مل'),
    ('mcg/ml', 'مكجم/مل'),
)

MEDICINE_DOSAGE_UNIT_CHOICES = (
    ('tablet', 'قرص'),
    ('capsule', 'كبسولة'),
    ('injection', 'حقنة'),
    ('syrup', 'شراب'),
    ('pill', 'حبة'),
)

MEDICINE_FREQUENCY_CHOICES = (
    ('as_needed', 'عند الحاجة'),
    ('once_daily', 'مرة يومياً'),
    ('twice_daily', 'مرتين يومياً'),
    ('thrice_daily', 'ثلاث مرات يومياً'),
    ('four_times_daily', 'اربع مرات يومياً'),
    ('five_times_daily', 'خمس مرات يومياً'),
    ('six_times_weekly', 'ست مرات اسبوعياً'),
    ('every_8_hours', 'كل 8 ساعات'),
    ('every_12_hours', 'كل 12 ساعة'),
    ('every_24_hours', 'كل 24 ساعة'),
)

MEDICINE_DURATION_UNIT_CHOICES = (
    ('days', 'أيام'),
    ('weeks', 'أسابيع'),
    ('months', 'أشهر'),
    ('years', 'سنوات'),
)

MEDICINE_ROUTE_CHOICES = (
    ('oral', 'فموي'),
    ('topical', 'موضعي'),
    ('inhalation', 'استنشاق'),
    ('injection', 'حقن'),
    ('rectal', 'شرجي'),
    ('vaginal', 'مهبلي'),
    ('ophthalmic', 'قطرات عيون'),
    ('otic', 'قطرات أذن'),
    ('nasal', 'بخاخ أنف'),
    ('sublingual', 'تحت اللسان'),
    ('transdermal', 'عبر الجلد'),
    ('intravenous', 'وريدي'),
    ('intramuscular', 'عضلي'),
    ('subcutaneous', 'تحت الجلد'),
)

MEDICINE_NOTES = (
    ('take_with_food', 'تناول مع الطعام'),
    ('take_on_empty_stomach', 'تناول على معدة فارغة'),
    ('before_sleep', 'قبل النوم'),
    ('after_waking', 'بعد الاستيقاظ'),
    ('with_meals', 'مع الوجبات'),
    ('between_meals', 'بين الوجبات'),
    ('before_meals', 'قبل الوجبات'),
    ('after_meals', 'بعد الوجبات'),    
    ('after_breakfast', 'بعد الفطور'),
    ('after_lunch', 'بعد الغداء'),
    ('after_dinner', 'بعد العشاء'),
    ('after_food', 'بعد الطعام'),
)