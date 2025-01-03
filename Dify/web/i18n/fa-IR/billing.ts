const translation = {
  currentPlan: 'طرح فعلی',
  upgradeBtn: {
    plain: 'ارتقاء طرح',
    encourage: 'هم اکنون ارتقاء دهید',
    encourageShort: 'ارتقاء دهید',
  },
  viewBilling: 'مدیریت صورتحساب‌ها و اشتراک‌ها',
  buyPermissionDeniedTip: 'لطفاً با مدیر سازمان خود تماس بگیرید تا اشتراک تهیه کنید',
  plansCommon: {
    title: 'یک طرح مناسب برای خود انتخاب کنید',
    yearlyTip: 'با اشتراک سالانه 2 ماه رایگان دریافت کنید!',
    mostPopular: 'محبوب‌ترین',
    planRange: {
      monthly: 'ماهانه',
      yearly: 'سالانه',
    },
    month: 'ماه',
    year: 'سال',
    save: 'صرفه‌جویی کنید ',
    free: 'رایگان',
    currentPlan: 'طرح فعلی',
    contractSales: 'تماس با فروش',
    contractOwner: 'تماس با مدیر تیم',
    startForFree: 'رایگان شروع کنید',
    getStartedWith: 'شروع کنید با ',
    contactSales: 'تماس با فروش',
    talkToSales: 'صحبت با فروش',
    modelProviders: 'ارائه‌دهندگان مدل',
    teamMembers: 'اعضای تیم',
    annotationQuota: 'سهمیه حاشیه‌نویسی',
    buildApps: 'ساخت اپلیکیشن‌ها',
    vectorSpace: 'فضای وکتور',
    vectorSpaceBillingTooltip: 'هر 1 مگابایت می‌تواند حدود 1.2 میلیون کاراکتر از داده‌های وکتور شده را ذخیره کند (براساس تخمین با استفاده از OpenAI Embeddings، متفاوت بر اساس مدل‌ها).',
    vectorSpaceTooltip: 'فضای وکتور سیستم حافظه بلند مدت است که برای درک داده‌های شما توسط LLM‌ها مورد نیاز است.',
    documentsUploadQuota: 'سهمیه بارگذاری مستندات',
    documentProcessingPriority: 'اولویت پردازش مستندات',
    documentProcessingPriorityTip: 'برای اولویت پردازش بالاتر مستندات، لطفاً طرح خود را ارتقاء دهید.',
    documentProcessingPriorityUpgrade: 'داده‌های بیشتری را با دقت بالاتر و سرعت بیشتر پردازش کنید.',
    priority: {
      'standard': 'استاندارد',
      'priority': 'اولویت',
      'top-priority': 'اولویت بالا',
    },
    logsHistory: 'تاریخچه گزارشات',
    customTools: 'ابزارهای سفارشی',
    unavailable: 'غیرقابل دسترس',
    days: 'روز',
    unlimited: 'نامحدود',
    support: 'پشتیبانی',
    supportItems: {
      communityForums: 'انجمن‌های اجتماعی',
      emailSupport: 'پشتیبانی ایمیل',
      priorityEmail: 'پشتیبانی ایمیل و چت با اولویت',
      logoChange: 'تغییر لوگو',
      SSOAuthentication: 'تأیید هویت SSO',
      personalizedSupport: 'پشتیبانی شخصی‌سازی شده',
      dedicatedAPISupport: 'پشتیبانی API اختصاصی',
      customIntegration: 'یکپارچه‌سازی و پشتیبانی سفارشی',
      ragAPIRequest: 'درخواست‌های API RAG',
      bulkUpload: 'بارگذاری دسته‌ای مستندات',
      agentMode: 'حالت Agent',
      workflow: 'جریان کار',
      llmLoadingBalancing: 'توزیع بار LLM',
      llmLoadingBalancingTooltip: 'اضافه کردن چندین کلید API به مدل‌ها، به طور مؤثر از محدودیت‌های نرخ API عبور می‌کند.',
    },
    comingSoon: 'به زودی',
    member: 'عضو',
    memberAfter: 'عضو',
    messageRequest: {
      title: 'اعتبارات پیام',
      tooltip: 'سهمیه‌های فراخوانی پیام برای طرح‌های مختلف با استفاده از مدل‌های OpenAI (به جز gpt4). پیام‌های بیش از حد محدودیت از کلید API OpenAI شما استفاده می‌کنند.',
    },
    annotatedResponse: {
      title: 'محدودیت‌های سهمیه حاشیه‌نویسی',
      tooltip: 'ویرایش دستی و حاشیه‌نویسی پاسخ‌ها، قابلیت‌های پرسش و پاسخ با کیفیت بالا و قابل تنظیم برای اپلیکیشن‌ها را فراهم می‌کند. (فقط در اپلیکیشن‌های چت اعمال می‌شود)',
    },
    ragAPIRequestTooltip: 'به تعداد درخواست‌های API که فقط قابلیت‌های پردازش پایگاه دانش Dify را فراخوانی می‌کنند اشاره دارد.',
    receiptInfo: 'فقط صاحب تیم و مدیر تیم می‌توانند اشتراک تهیه کنند و اطلاعات صورتحساب را مشاهده کنند',
  },
  plans: {
    sandbox: {
      name: 'محیط آزمایشی',
      description: '200 بار آزمایش رایگان GPT',
      includesTitle: 'شامل:',
    },
    professional: {
      name: 'حرفه‌ای',
      description: 'برای افراد و تیم‌های کوچک برای باز کردن قدرت بیشتر به طور مقرون به صرفه.',
      includesTitle: 'همه چیز در طرح رایگان، به علاوه:',
    },
    team: {
      name: 'تیم',
      description: 'همکاری بدون محدودیت و لذت بردن از عملکرد برتر.',
      includesTitle: 'همه چیز در طرح حرفه‌ای، به علاوه:',
    },
    enterprise: {
      name: 'سازمانی',
      description: 'دریافت کامل‌ترین قابلیت‌ها و پشتیبانی برای سیستم‌های بزرگ و بحرانی.',
      includesTitle: 'همه چیز در طرح تیم، به علاوه:',
    },
  },
  vectorSpace: {
    fullTip: 'فضای وکتور پر است.',
    fullSolution: 'طرح خود را ارتقاء دهید تا فضای بیشتری دریافت کنید.',
  },
  apps: {
    fullTipLine1: 'طرح خود را ارتقاء دهید تا',
    fullTipLine2: 'اپلیکیشن‌های بیشتری بسازید.',
  },
  annotatedResponse: {
    fullTipLine1: 'طرح خود را ارتقاء دهید تا',
    fullTipLine2: 'مکالمات بیشتری را حاشیه‌نویسی کنید.',
    quotaTitle: 'سهمیه پاسخ حاشیه‌نویسی',
  },
}

export default translation
