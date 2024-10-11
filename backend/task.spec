# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs
import os
import sys

project_root = os.path.abspath(os.path.dirname(sys.argv[0]))

# 自动收集 'app' 和 'asyncpg' 的所有子模块
app_submodules = collect_submodules('app')
asyncpg_submodules = collect_submodules('asyncpg')

# 收集 'asyncpg' 的动态库
asyncpg_binaries = collect_dynamic_libs('asyncpg')

a = Analysis(
    ['app/service/task/celery_app.py'],
    pathex=[project_root],
    binaries=[],
    datas=[],
    hiddenimports=app_submodules + asyncpg_submodules + [
        'celery.fixups',
        'celery.backends',
        'celery.concurrency',
        'celery.worker',
        'celery.fixups.django',
        'celery.loaders.app',
        'celery.concurrency.prefork',
        'celery.apps.worker',
        'celery.app.log',
        'celery.app.amqp',
        'celery.worker.components',
        'celery.worker.consumer',
        'celery.worker.autoscale',
        'celery.worker.autoscale',
        'celery.app.control',
        'celery.app.events',
        'celery.events.state',
        'celery.backends.redis',
        'celery.worker.strategy',
        'celery.fixups.django',
        'celery.loaders.app',
        'app.service.task.rag',
        'app.service.task.rag.task',
        'asyncpg.pgproto.pgproto',
        'eventlet.hubs.epolls',
        'eventlet.hubs.kqueue',
        'eventlet.hubs.selects',
        'dns.dnssec',
        'dns.namedict'
    ],
    hookspath=['./hooks'],               # 指向自定义的 hook 文件
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='task',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='task',
)
