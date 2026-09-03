Set-Location C:\ai\loop
python C:\ai\loop\loop.py --backend llama --init json_worse --steps 40 --max-tokens 4096 --stop-on-cycle --out C:\ai\loop\site\runs_extra\qwen_worse_4k *> C:\ai\loop\site\runs_extra\qwen_worse_4k.log
python C:\ai\loop\loop.py --backend llama --init json_unexpected --steps 40 --max-tokens 4096 --stop-on-cycle --out C:\ai\loop\site\runs_extra\qwen_unexpected_4k *> C:\ai\loop\site\runs_extra\qwen_unexpected_4k.log
