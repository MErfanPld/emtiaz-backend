"""ثابت‌های مشترک مجموعه املاک امتیاز."""


class Department:
    """بخش‌های عملیاتی مجموعه."""

    RENT = 'rent'
    SALE = 'sale'
    KOLANGI = 'kolangi'
    PARTNERSHIP = 'partnership'
    MOSTAGHELAT = 'mostaghelat'

    CHOICES = [
        (RENT, 'رهن و اجاره'),
        (SALE, 'خرید و فروش'),
        (KOLANGI, 'کلنگی'),
        (PARTNERSHIP, 'مشارکت در ساخت'),
        (MOSTAGHELAT, 'مستقلات'),
    ]

    CHOICES_EN = {
        RENT: 'Rent & Lease',
        SALE: 'Buy & Sell',
        KOLANGI: 'Old / Redevelopment',
        PARTNERSHIP: 'Construction Partnership',
        MOSTAGHELAT: 'Standalone Properties',
    }

    # نام گروه جنگو متناظر (برای همگام‌سازی نقش)
    GROUP_NAMES = {
        RENT: 'رهن و اجاره',
        SALE: 'خرید و فروش',
        KOLANGI: 'کلنگی',
        PARTNERSHIP: 'مشارکت در ساخت',
        MOSTAGHELAT: 'مستقلات',
    }


SLOGAN_FA = 'انتخاب شما امتیاز ماست'
SLOGAN_EN = 'Your choice is our distinction'
