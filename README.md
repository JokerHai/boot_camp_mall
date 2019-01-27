数据库操作外键：
	
	在设置外键时，需要通过on_delete选项指明主表删除数据时，对于外键引用表数据如何处理.
	
	在django.db.models中包含了可选常量：
	
		​CASCADE 级联，删除主表数据时连通一起删除外键表中数据

		​PROTECT 保护，通过抛出ProtectedError异常，来阻止删除主表中被外键应用的数据

		​SET_NULL 设置为NULL，仅在该字段null=True允许为null时可用



