#!/usr/bin/env python3
"""Create a disposable local Git repository for skill evaluation."""
import argparse
from pathlib import Path
import subprocess

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    root=args.output.expanduser().resolve()
    if root.exists(): p.error('The output path must not exist.')
    root.mkdir(parents=True)
    def put(name,body): (root/name).write_text(body,encoding='utf-8')
    def git(*args): subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    put('shop.py','''def total_cents(unit_cents, quantity):
    if unit_cents < 0 or quantity < 0:
        raise ValueError("nonnegative values required")
    return unit_cents * quantity


def visible_orders(orders, tenant_id):
    return [order for order in orders if order["tenant_id"] == tenant_id]
''')
    put('test_shop.py','''import unittest
from shop import total_cents, visible_orders

class ShopTests(unittest.TestCase):
    def test_total(self): self.assertEqual(1500, total_cents(500,3))
    def test_negative(self):
        with self.assertRaises(ValueError): total_cents(-1,1)
    def test_tenant_boundary(self):
        orders=[{"tenant_id":"a","id":1},{"tenant_id":"b","id":2}]
        self.assertEqual([orders[0]],visible_orders(orders,"a"))

if __name__ == "__main__": unittest.main()
''')
    put('README.md','# Shop fixture\n\nPrices are integer cents. Total is unit price multiplied by quantity. Order reads are tenant-scoped. Run `python3 -m unittest -v`.\n')
    put('.gitignore','__pycache__/\n')
    git('init','-b','main');git('config','user.name','Vibe Coding Fixture');git('config','user.email','fixture@example.invalid')
    git('add','.');git('commit','-m','Add shop contract and tests');git('checkout','-b','review-example')
    put('shop.py',(root/'shop.py').read_text(encoding='utf-8').replace('return unit_cents * quantity','return unit_cents + quantity'))
    git('add','shop.py');git('commit','-m','Change total calculation')
    put('README.md',(root/'README.md').read_text(encoding='utf-8')+'\nOrder identifiers are stable within a tenant.\n')
    git('add','README.md');git('commit','-m','Document order identifiers')
    print(root)

if __name__=='__main__':main()
