SIM = vcs

RTL = rtl_codes/down_counter.sv rtl_codes/dc_interface.sv
TB  = rtl_codes/env.sv rtl_codes/tb_top.sv

OUT = simv

compile:
	$(SIM) -full64 -sverilog $(RTL) $(TB) -o $(OUT)

run:
	./$(OUT) +tests=50 | tee run.log

regress:
	mkdir -p logs results waves
	@for i in 1 2 3 4 5; do \
		echo "Run $$i"; \
		./$(OUT) +tests=50 | tee logs/run_$$i.log; \
		mv results.csv results/results_$$i.csv; \
	done

clean:
	rm -rf csrc simv simv.daidir ucli.key logs results waves *.log
