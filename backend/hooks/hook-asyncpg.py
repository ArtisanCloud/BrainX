from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

# 合并所有的隐藏导入
# 合并所有的隐藏导入
hiddenimports = (
    collect_submodules('asyncpg') +
    collect_submodules('dns') +
    collect_submodules('celery')
)

binaries = collect_dynamic_libs('asyncpg')
