#!/usr/bin/env python

import asyncio

from NotiConsumer import NotiConsumer

def main():
    consumer = NotiConsumer()
    consumer.connect_rabbit()
    
if __name__ == '__main__':
    asyncio.run(main())