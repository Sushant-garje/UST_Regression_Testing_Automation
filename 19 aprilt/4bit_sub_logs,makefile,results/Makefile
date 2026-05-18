SIM = vcs

RTL = rtl/subtractor.sv rtl/sub_interface.sv
TB  = rtl/env.sv rtl/tb_top.sv

OUT = simv

compile:
	$(SIM) -full64 -sverilog $(RTL) $(TB) -o $(OUT)

run:
	./$(OUT) +seed=1 +tests=100 | tee run.log

regress:
	mkdir -p logs results waves
	@for i in 1 2 3 4 5; do \
		echo "Running Seed $$i"; \
		./$(OUT) +seed=$$i +tests=500 | tee logs/run_$$i.log; \
		mv results.csv results/results_$$i.csv; \
	done

clean:
	rm -rf csrc simv simv.daidir ucli.key logs results waves *.log
