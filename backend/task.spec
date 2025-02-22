# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs
import os
import sys

project_root = os.path.abspath(os.path.dirname(sys.argv[0]))

import emoji
import unstructured

emoji_json_path = os.path.join(emoji.__path__[0], 'unicode_codes', 'emoji.json')
words_file_path = os.path.join(os.path.dirname(unstructured.__file__), 'nlp', 'english-words.txt')

# 自动收集 'app' 和 'asyncpg' 的所有子模块
app_submodules = collect_submodules('app')
asyncpg_submodules = collect_submodules('asyncpg')
gevent_submodules = collect_submodules('gevent')

# 收集 'asyncpg' 的动态库
asyncpg_binaries = collect_dynamic_libs('asyncpg')

a = Analysis(
    ['app/service/task/celery_worker.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        (emoji_json_path, 'emoji/unicode_codes'),
        (words_file_path, 'unstructured/nlp')
    ],
    hiddenimports=app_submodules + asyncpg_submodules + gevent_submodules +  [
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
        'celery.backends.database',
        'app.service.task.task',
        'app.service.task.celery_worker',
        'app.service.task.rag',
        'app.service.task.rag.task',
        'asyncpg.pgproto.pgproto',
        'eventlet.hubs.epolls',
        'eventlet.hubs.kqueue',
        'eventlet.hubs.selects',
        'pydantic.deprecated.decorator',
        'numpy.distutils',
        'kombu.transport.pyamqp',
        'dns.dnssec',
        'dns.namedict',
        # pro

        #custom

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
